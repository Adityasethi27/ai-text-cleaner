# AI Text Cleaner 🎬

An AI-powered REST API that takes messy, unstructured text about movies and converts it into clean, structured data saved to a database. Built with FastAPI and Google's Gemini API.

## What it does

Send the API messy human text like:

> "got interstellar great movie by nolan came out 2014 I'd give it 9 out of 10 also watched the dark knight rises which was decent maybe 7.5"

...and it returns clean, structured JSON, automatically saved to a database:

```json
{
  "movies_saved": 2,
  "data": [
    {"title": "Interstellar", "director": "Christopher Nolan", "year": 2014, "rating": 9.0},
    {"title": "The Dark Knight Rises", "director": "Christopher Nolan", "year": 2012, "rating": 7.5}
  ]
}
```

## Tech Stack

- **FastAPI** — web framework for the REST API
- **SQLAlchemy** — ORM for database operations
- **SQLite** — lightweight database
- **Google Gemini API** — LLM for text extraction
- **Pydantic** — request validation

## API Endpoints

| Method | Endpoint    | Description                                  |
|--------|-------------|----------------------------------------------|
| GET    | `/`         | Health check                                 |
| POST   | `/extract`  | Send messy text → get clean data saved to DB |
| GET    | `/movies`   | List all movies saved in the database        |

## Setup

```bash
git clone https://github.com/Adityasethi27/ai-text-cleaner.git
cd ai-text-cleaner
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy requests python-dotenv
echo "GEMINI_API_KEY=your_key_here" > .env
uvicorn ai_movie_api:app --reload
```

Then open `http://127.0.0.1:8000/docs` to try the interactive API.

## What I learned building this

- Calling an external LLM API from Python and parsing nested JSON responses
- Prompt engineering techniques (few-shot examples) for reliable structured output
- Combining a web framework, an ORM, and an AI API into one working pipeline
- Handling the realities of AI APIs (rate limits, retries, non-deterministic output)
