from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# A reusable prompt with a system message (the AI's role) and a human message (the input)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise tech tutor. Explain things in exactly 2 sentences, no more. Use simple analogies."),
    ("human", "Explain {topic} to a complete beginner.")
])

# Fill in the blank and send it
chain = prompt | llm

# {topic} gets filled here — and you can reuse this for ANY topic
response = chain.invoke({"topic": "what an API is"})
print(response.content)

print("\n---\n")

# Reuse the SAME template with a different topic — no rewriting the prompt
response2 = chain.invoke({"topic": "what a database index is"})
print(response2.content)
