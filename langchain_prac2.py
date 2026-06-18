from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import List 
from dotenv import load_dotenv
import os

load_dotenv()

class Recipe(BaseModel):
    name : str = Field(description="enter name of the dish")
    cuisine : str = Field(description="enter the cuisine of the dish")
    prep_time_minutes : int = Field(description = " time taken to prepare the dish")
    difficulty : str = Field(description="difficulty level of the dish")
    main_ingredients: List[str] = Field(description="List of the main ingredients")    

    
class RecipeList(BaseModel):
    recipes: List[Recipe] = Field(description="List of all recipes found in the text")
    
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = os.getenv("GEMINI_API_KEY")
)

structured_llm = llm.with_structured_output(RecipeList)

messy_text = input ("Enter text here")
result = structured_llm.invoke(f"Extract every recipe in the text, do not skip any : {messy_text}")

print(f"\nFound {len(result.recipes)} main ingredients:\n")

for recipe in result.recipes:
    print(f" name of the dish is {recipe.name}, its cuisine is {recipe.cuisine}, it takes {recipe.prep_time_minutes} mins to prepare and is {recipe.difficulty} to make")
    
