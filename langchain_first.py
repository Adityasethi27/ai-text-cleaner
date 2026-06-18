from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# Create the LLM object — this replaces ALL the url/payload plumbing
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Ask it something — one clean line
response = llm.invoke("Explain what an API is in exactly 2 sentences.")

# The answer is in .content
print(response.content)
