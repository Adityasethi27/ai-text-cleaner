from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()

# --- The data shape ---
class Movie(BaseModel):
    title: str = Field(description="Full official movie title")
    director: str = Field(description="Full name of director")
    year: int = Field(description="Year released")
    rating: Optional[float] = Field(default=None, description="Rating out of 10, or None if not mentioned")

class MovieList(BaseModel):
    movies: List[Movie] = Field(description="All movies found in the text")

# --- The LLM with structured output ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
structured_llm = llm.with_structured_output(MovieList)

# --- A reusable prompt: system message sets the rules, human provides the data ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a meticulous data extraction engine. Extract EVERY item mentioned, never skip any. Never invent data that isn't present or inferable. If a rating isn't given, leave it null."),
    ("human", "Extract all movies from this text: {text}")
])

# --- Chain it: prompt -> structured LLM ---
chain = prompt | structured_llm

messy_text = input("Paste messy movie data: ")
result = chain.invoke({"text": messy_text})

print(f"\nFound {len(result.movies)} movies:\n")
for movie in result.movies:
    rating = movie.rating if movie.rating is not None else "not rated"
    print(f"  {movie.title} ({movie.year}) — dir. {movie.director}, rating: {rating}")
