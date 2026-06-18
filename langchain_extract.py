from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

# --- Step 1: Define the shape we want, using Pydantic (just like FastAPI!) ---
class Movie(BaseModel):
    title: str = Field(description="Full official movie title, properly capitalized")
    director: str = Field(description="Full name of director, e.g. 'Christopher Nolan'")
    year: int = Field(description="Year the movie was released")
    rating: float = Field(description="Rating out of 10")

class MovieList(BaseModel):
    movies: List[Movie] = Field(description="List of all movies found in the text")

# --- Step 2: Create the LLM and tell it to return our structure ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# This one line replaces the prompt-begging + json.loads + try/except!
structured_llm = llm.with_structured_output(MovieList)

# --- Step 3: Just invoke with the messy text ---
messy_text = input("Paste messy movie data: ")
result = structured_llm.invoke(f"Extract EVERY movie mentioned in this text, do not skip any: {messy_text}")

# --- Step 4: result is already a Python object, no parsing needed ---
print(f"\nFound {len(result.movies)} movies:\n")
for movie in result.movies:
    print(f"  {movie.title} ({movie.year}) — dir. {movie.director}, rated {movie.rating}/10")
