import os

import google.genai as genai
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

class RequestData(BaseModel):
    prompt: str
    max_length: int = 2000

@app.post("/geminiask")
def generate_ans(data: RequestData):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing from the environment or .env file")

    client = genai.Client(api_key=api_key)