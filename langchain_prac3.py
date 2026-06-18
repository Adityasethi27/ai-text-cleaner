from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import List 
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

class Job_Application(BaseModel):
    company : str = Field(description = "enter the company mentioned" )
    role: str = Field(description="enter the role mentioned")
    salary_lpa: Optional[float] = Field(default=None, description="Salary in lakhs per annum, or None if not mentioned")
    location : str = Field(description = "enter the field mentioned")
    deadline : str = Field(description = "enter the deadline mentioned ")
    
class Job_Application_List(BaseModel):
    Job_Applications: List[Job_Application] = Field(description = "List of all jobs mentioned in the job applications")
    
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = os.getenv("GEMINI_API_KEY")
    
)

structured_llm = llm.with_structured_output(Job_Application_List)

messy_text = input("Enter the Job Appliation here : ")
result = structured_llm.invoke(f"Extract every application and its details in the text, do not miss any: {messy_text}")

print(f"\n found {len(result.Job_Applications)} in the given text \n")
for application in result.Job_Applications :
    print(f""" company - {application.company},
             current role - {application.role},
             salary_lpa - {application.salary_lpa}, 
             location - {application.location},
             deadline - {application.deadline}"""
)
    