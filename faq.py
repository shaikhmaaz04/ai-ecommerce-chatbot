# faq.py

from pathlib import Path
import pandas as pd
import chromadb
import os
from groq import Groq
from dotenv import load_dotenv
from chromadb.utils import embedding_functions

load_dotenv()

faqs_path = str(Path(__file__).parent / "resources/faq_data.csv")
chroma_path = str(Path(__file__).parent / "vector_store/")
chroma_client = chromadb.PersistentClient(path=chroma_path)
collection_name_faq = "faqs"
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=embedding_model
)
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ingest_faq_data(path):
    if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:

        collection = chroma_client.get_or_create_collection(
            name=collection_name_faq,
            embedding_function=ef
            )
        
        df = pd.read_csv(path)
        docs = df["question"].to_list()
        metadata = [{"answer": answer} for answer in df["answer"].to_list()]

        collection.add(
            documents=docs,
            metadatas=metadata,
            ids=[f"id_{i+1}" for i in range(len(docs))]
        )
        print(f"FAQ Data Successfully ingested into ChromaDB Collection: {collection_name_faq}")
    else:
        print(f"Collection {collection_name_faq} already exists!")

def get_relevant_qa(query):
    collection = chroma_client.get_collection(collection_name_faq)

    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    return results

def faq_chain(query):
    results = get_relevant_qa(query)
    context = " ".join([r.get("answer") for r in results['metadatas'][0]])
    answer = generate_answer(query, context)
    return answer

def generate_answer(query, context):
    prompt = f"""
    ACT AS A PROFESSIONAL CUSTOMER SUPPORT AGENT.

    Given the question and context, provide a professional answer based on the context only. If you can't find the answer inside the context then just say 'Sorry, I do not know.'.
    Don't make things up.

    Question: {query}

    CONTEXT: {context}
    """

    chat_completion = groq_client.chat.completions.create(

        messages=[
            {
                "role": "user",
                "content": prompt,
            }

        ],

        model=os.environ.get("GROQ_MODEL"),
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    print(faqs_path)
    ingest_faq_data(faqs_path)

    # query = "What is your return policy on defective products?"
    query = "Do you take cash as a payment option?"

    results = get_relevant_qa(query)
    print(results)

    answer = faq_chain(query)
    print(answer)