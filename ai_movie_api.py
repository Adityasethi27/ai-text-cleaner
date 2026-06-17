from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import requests as http_requests
import json
from dotenv import load_dotenv
import os

# --- Load API key ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

# --- Database setup (same as Phase 1!) ---
engine = create_engine("sqlite:///./ai_movies.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    director = Column(String)
    year = Column(Integer)
    rating = Column(Float)

Base.metadata.create_all(bind=engine)

# --- Pydantic schema ---
class MessyInput(BaseModel):
    text: str

# --- FastAPI app ---
app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Movie API — send messy text, get clean database entries"}

@app.post("/extract")
def extract_movies(data: MessyInput):
    # Step 1: Build the prompt
    prompt = f"""Extract ALL movie information from the following messy text.
Return ONLY a valid JSON array. No explanation, no markdown, no code fences.
Do NOT skip any movie mentioned, even if some details are missing.

Each movie object must have exactly these fields:
- "title": string (full official title, properly capitalized)
- "director": string (full name)
- "year": integer
- "rating": float (out of 10)

EXAMPLE:
Input: "saw oppenheimer last week by nolan 2023 loved it 9.5 and barbie was fun too greta gerwig 7"
Output: [{{"title": "Oppenheimer", "director": "Christopher Nolan", "year": 2023, "rating": 9.5}}, {{"title": "Barbie", "director": "Greta Gerwig", "year": 2023, "rating": 7.0}}]

Now extract from this text:
{data.text}"""

    # Step 2: Call Gemini
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = http_requests.post(GEMINI_URL, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Gemini API error: {response.status_code}")

    raw = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    # Step 3: Parse the AI response
    try:
        movies_data = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="AI returned invalid JSON")

    # Step 4: Save to database
    db = SessionLocal()
    saved = []
    for m in movies_data:
        movie = Movie(
            title=m["title"],
            director=m["director"],
            year=m["year"],
            rating=m["rating"]
        )
        db.add(movie)
        saved.append(m)
    db.commit()
    db.close()

    return {"movies_saved": len(saved), "data": saved}

@app.get("/movies")
def list_movies():
    db = SessionLocal()
    movies = db.query(Movie).all()
    db.close()
    return movies
