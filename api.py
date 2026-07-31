from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()  # Used locally

app = FastAPI()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)

class Prompt(BaseModel):
    question: str

@app.get("/process")
def process():
    return {"response": "Processed successfully"}

@app.post("/ask")
def ask(prompt: Prompt):
    response = llm.invoke(prompt.question)
    return {"answer": response.content}