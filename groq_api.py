import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key = GROQ_API_KEY)

with open("prompt.txt") as f:
    PROMPT = f.read()

def ask_groq(content: str):
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

def ask_groq_prompt(text: str):
    return ask_groq(PROMPT + text)

if __name__ == "__main__":
    print(ask_groq("As concise as possible, what is a React component?"))
