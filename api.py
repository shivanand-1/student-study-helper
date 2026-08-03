from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
import os

load_dotenv()

app = FastAPI()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)

# Store extracted PDF text
pdf_text = ""


class Prompt(BaseModel):
    question: str
    isquestions:str


@app.get("/")
def home():
    return {"message": "API Running Successfully"}


@app.post("/process")
async def process(file: UploadFile = File(...)):
    global pdf_text


    loader = PyPDFLoader(file.filename)
    docs = loader.load()

    pdf_text = "\n".join(doc.page_content for doc in docs)

    return {
        "message": "PDF processed successfully",
        "pages": pdf_text
    }


@app.post("/ask")
def ask(prompt: Prompt):
    global pdf_text

    if pdf_text == "":
        return {
            "error": "Please upload a PDF first."
        }

    full_prompt = f"""
You are an AI assistant.

Answer the question using ONLY the following PDF content.

PDF Content:
{pdf_text}

Question:
{prompt.question}
"""

    response = llm.invoke(full_prompt)

    return {
        "answer": response.content
    }