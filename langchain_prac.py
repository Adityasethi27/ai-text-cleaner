from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import List 
from dotenv import load_dotenv
import os

load_dotenv()

class Book(BaseModel):
    title : str = Field(description = "Full official title of the book, Properely Capitalized")
    name : str = Field(description = "Full name of the author, e.g Ruskin Bond")
    genre : str = Field(description = "Describe genre of the book, e.g genre of The Lord of the Rings is Fiction, genre of Dune is Science Fiction, genre of Pride and Prejudice is romance")
    pages : int = Field(description = "Total number of pages of a book")
    rating : float = Field(description="Rating out of 10")
    year : int = Field(description = "The year in which the book was released")

class BookList(BaseModel):
    books:List[Book] = Field(description = "List of all the books found in text")
    
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = os.getenv("GEMINI_API_KEY")
 )

structured_llm = llm.with_structured_output(BookList)

messy_text = input("enter text here")
result = structured_llm.invoke(f"Extract every book in the text, do not skip any : {messy_text}")

print(f"\nFound {len(result.books)} books:\n")
for book in result.books :
    print(f". {book.title} released in {book.year} written by {book.name}, it has {book.pages} and its  Genre is {book.genre} with a rating - {book.rating}")
    