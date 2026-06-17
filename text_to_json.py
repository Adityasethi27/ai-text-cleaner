import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

# The messy input (later this could come from a user, a file, or an API)
messy_text = input("Paste messy movie data: ")

# The prompt — THIS is where prompt engineering matters
prompt = f"""Extract ALL movie information from the following messy text.
Return ONLY a valid JSON array. No explanation, no markdown, no code fences.
Do NOT skip any movie mentioned, even if some details are missing.

Each movie object must have exactly these fields:
- "title": string (full official title, properly capitalized)
- "director": string (full name — e.g. "Christopher Nolan" not just "Nolan")
- "year": integer
- "rating": float (out of 10)

EXAMPLE:
Input: "saw oppenheimer last week by nolan 2023 loved it 9.5 and barbie was fun too greta gerwig 7"
Output: [{{"title": "Oppenheimer", "director": "Christopher Nolan", "year": 2023, "rating": 9.5}}, {{"title": "Barbie", "director": "Greta Gerwig", "year": 2023, "rating": 7.0}}]

Now extract from this text:
{messy_text}"""
payload = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ]
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    raw_answer = data["candidates"][0]["content"]["parts"][0]["text"]
    
    # Parse the JSON the AI returned
    try:
        movies = json.loads(raw_answer)
        print("\nExtracted movies:")
        print(json.dumps(movies, indent=2))
        print(f"\nFound {len(movies)} movies ready for your database!")
    except json.JSONDecodeError:
        print("\nAI returned something that wasn't valid JSON:")
        print(raw_answer)
else:
    print(f"Error {response.status_code}:")
    print(response.text)
