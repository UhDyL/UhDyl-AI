from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()
OLLAMA_API = os.getenv("OLLAMA_API", "http://localhost:11434")

class GenerateRequest(BaseModel):
    prompt: str
    images: list[str] | None = None

@app.post("/generate")
def generate(req: GenerateRequest):
    model = "llava-llama3:8b" if req.images else "llama3"

    payload = {
        "model": model,
        "prompt": req.prompt
    }

    if req.images:
        payload["images"] = req.images

    res = requests.post(f"{OLLAMA_API}/api/generate", json=payload)
    return res.json()
