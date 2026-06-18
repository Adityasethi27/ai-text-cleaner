from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise tech tutor. Answer in 2 sentences."),
    ("human", "Explain {topic} to a beginner.")
])

chain = prompt | llm

# This decorator wraps the function with retry logic
@retry(
    stop=stop_after_attempt(4),                    # try max 4 times
    wait=wait_exponential(min=2, max=20),          # wait 2s, then 4s, then 8s... up to 20s
    retry=retry_if_exception_type(Exception),      # retry on any exception
    reraise=True                                    # if all retries fail, raise the last error
)
def ask_with_retry(topic):
    print(f"  → Calling AI for topic: {topic}")
    response = chain.invoke({"topic": topic})
    return response.content

# Try it
try:
    answer = ask_with_retry("what a database transaction is")
    print(f"\n{answer}\n")
except Exception as e:
    print(f"\nAll retries failed: {e}")
