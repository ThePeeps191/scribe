import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key = GROQ_API_KEY)

def ask_groq(content: str) -> str:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content" : content
            }
        ],
        model="openai/gpt-oss-20b",
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    print(ask_groq("return the following with corrected grammar: hi im bob and i like to watch youtube"))
