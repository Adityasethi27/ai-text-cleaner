import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Ask the user for their prompt
user_prompt = input("Ask Gemini anything: ")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

payload = {
    "contents": [
        {
            "parts": [
                {"text": user_prompt}
            ]
        }
    ]
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    answer = data["candidates"][0]["content"]["parts"][0]["text"]
    print("\n" + answer)
else:
    print(f"Error {response.status_code}:")
    print(response.text)