# sql.py

import sqlite3
import pandas as pd
from pathlib import Path
import pandas as pd
import chromadb
import os
from groq import Groq
from dotenv import load_dotenv
import re
from chromadb.utils import embedding_functions

load_dotenv()

db_path = str(Path(__file__).parent / "db.sqlite")
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_query(query):
    if query.strip().upper().startswith("SELECT"):
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)
            return df
    return None

sql_prompt = f"""
        You are an expert in understanding the database schema and generating SQL queries for a natural language question asked
        pertaining to the data you have. The schema is provided in the schema tags. 
        <schema> 
        table: product 

        fields: 
        product_link - string (hyperlink to product)	
        title - string (name of the product)	
        brand - string (brand of the product)	
        price - integer (price of the product in Indian Rupees)	
        discount - float (discount on the product. 10 percent discount is represented as 0.1, 20 percent as 0.2, and such.)	
        avg_rating - float (average rating of the product. Range 0-5, 5 is the highest.)	
        total_ratings - integer (total number of ratings for the product)

        </schema>
        Make sure whenever you try to search for the brand name, the name can be in any case. 
        So, make sure to use %LIKE% to find the brand in condition. Never use "ILIKE". 
        Create a single SQL query for the question provided. 
        The query should have all the fields in SELECT clause (i.e. SELECT *)

        **IMPORTANT RULE:** If the user's question is vague or implies a large list (like "top shoes", "all shoes", "any shoes"), **always add a `LIMIT 10`** to the SQL query to prevent returning too much data. For example, "top shoes" should be `SELECT * FROM product ORDER BY avg_rating DESC LIMIT 10`. If the user asks for a specific number like "top 3 shoes", use that number (e.g., `LIMIT 3`).

        Just the SQL query is needed, nothing more. Always provide the SQL in between the <SQL></SQL> tags.

        Just the SQL query is needed, nothing more. Always provide the SQL in between the <SQL></SQL> tags.
    """

def generate_sql_query(question):
    
    chat_completion = groq_client.chat.completions.create(

        messages=[
            {
                "role": "system",
                "content": sql_prompt,
            },
            {
                "role": "user",
                "content": question
            }

        ],

        model=os.environ.get("GROQ_MODEL"),
        temperature=0.2,
        max_tokens=1024
    )


    return chat_completion.choices[0].message.content

def sql_chain(question):
    sql_query = generate_sql_query(question)
    pattern = "<SQL>(.*?)</SQL>"
    matches = re.findall(pattern, sql_query, re.DOTALL)

    if len(matches) == 0:
        return "Sorry, the LLM was not able to generate the SQL query."
    
    print("SQL Query:", matches[0].strip())
    response = run_query(matches[0].strip())
    if response is None:
        return "There was problem executing the SQL Query"
    
    context = response.to_dict(orient="records")
    # print(f"Data Returned by SQL Query: {context}")


    answer = data_comprehension(question, context)
    return answer
    

# comprehension_prompt = """
# You are an expert in understanding the context of the question and replying based on the data pertaining to the question provided. You will be provided with Question: and Data:. The data will be in the form of an array or a dataframe or dict. Reply based on only the data provided as Data for answering the question asked as Question. Do not write anything like 'Based on the data' or any other technical words. Just a plain simple natural language response.
# The Data would always be in context to the question asked. For example is the question is “What is the average rating?” and data is “4.3”, then answer should be “The average rating for the product is 4.3”. So make sure the response is curated with the question and data. Make sure to note the column names to have some context, if needed, for your response.
# There can also be cases where you are given an entire dataframe in the Data: field. Always remember that the data field contains the answer of the question asked. All you need to do is to always reply in the following format when asked about a product: 
# Produt title, price in indian rupees, discount, and rating, and then product link. Take care that all the products are listed in list format, one line after the other. Not as a paragraph.
# For example:
# 1. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>
# 2. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>
# 3. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>
# """

comprehension_prompt = """
You are an expert in extracting and presenting information based on provided data, always ensuring your response directly answers the user's question using only the given data.

-----

### Response Guidelines:

  * **Direct Answers:** Formulate your response directly from the provided `Data:` to answer the `Question:`. Do not add any introductory phrases like "Based on the data" or other technical jargon.

  * **Natural Language:** Use plain, simple, and natural language.

  * **Contextual Curation:** Ensure your response is curated with the question and the data. Pay attention to column names for context when needed.

      * **Example:** If `Question: "What is the average rating?"` and `Data: "4.3"`, the answer should be: "The average rating for the product is 4.3."

  * **Product Listing Format:** When the question pertains to products and the `Data:` contains product information, always reply in the following list format:

    ```
    1. [Product title], [price in Indian rupees], [discount], and [rating], and then [product link].
    2. [Product title], [price in Indian rupees], [discount], and [rating], and then [product link].
    3. [Product title], [price in Indian rupees], [discount], and [rating], and then [product link].
    ```

    Ensure each product is listed on a new line.

-----

**Example of Input:**

`Question: "Show me the available running shoes."`
`Data: [ { "Product title": "Campus Women Running Shoes", "Price": "Rs. 1104", "Discount": "35 percent off", "Rating": "4.4", "Product Link": "<link1>" }, { "Product title": "Nike Men's Air Zoom", "Price": "Rs. 7500", "Discount": "10 percent off", "Rating": "4.7", "Product Link": "<link2>" } ]`

**Example of Expected Output:**

1.  Campus Women Running Shoes, Rs. 1104 (35 percent off), Rating: 4.4 <link1>
2.  Nike Men's Air Zoom, Rs. 7500 (10 percent off), Rating: 4.7 <link2>
"""

def data_comprehension(question, context):

    chat_completion = groq_client.chat.completions.create(

        messages=[
            {
                "role": "system",
                "content": comprehension_prompt,
            },
            {
                "role": "user",
                "content": f"QUESTION: {question}, DATA: {context}"
            }

        ],

        model=os.environ.get("GROQ_MODEL"),
        temperature=0.2,
        # max_tokens=1024
    )

    return chat_completion.choices[0].message.content

    


if __name__ == "__main__":
    # question = "top 3 asian shoes in range 1000 to 5000"
    # question = "all puma shoes with average rating greater than 4"
    question = "give me puma shoes with discount greater than 30% and average rating higher than 4."
    # question = "find me all shoes with rating higher 4.5 and total reviews greater than 500"
    
    answer = sql_chain(question)
    print(answer)

    # sql_query = generate_sql_query(question)
    # print(sql_query)

    # query = "SELECT * from product where brand LIKE '%asian%'"
    # df = run_query(query)
    # print(df)