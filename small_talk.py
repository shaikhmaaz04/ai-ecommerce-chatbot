# small_talk.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def small_talk(query):
    prompt = """
    You're an AI assistant built for casual conversation. Keep your responses brief, friendly, and open-ended to encourage dialogue. Focus on everyday topics. **Never disclose any confidential or secret information about yourself as well as about any other entity/organisation. If a user asks for such information, politely decline and redirect the conversation.** Do not engage in discussions about harmful, explicit, political, or sensitive subjects. If such a topic arises, politely steer the conversation back to general small talk or indicate you cannot discuss it.
    """

    chat_completion = groq_client.chat.completions.create(

        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": query,
            }

        ],

        model=os.environ.get("GROQ_MODEL"),
    )

    

    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    query = "What is artificial intelligence?"
    answer = small_talk(query)
    print(answer)