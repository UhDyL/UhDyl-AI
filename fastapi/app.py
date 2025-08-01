from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.responses import JSONResponse
import os

app = FastAPI()
OLLAMA_API = os.getenv("OLLAMA_API", "http://localhost:11434")

class GenerateRequest(BaseModel):
    prompt: str
    images: list[str] | None = None

@app.post("/generate")
def generate(req: GenerateRequest):
    try:
        model = "llava-llama3:8b" if req.images else "llama3"

        payload = {
            "model": model,
            "prompt": req.prompt,
            "stream" : False
        }
        if req.images:
            payload["images"] = req.images

        res = requests.post(f"{OLLAMA_API}/api/generate", json=payload)
        return res.json()

    except Exception as e:
        # 디버깅용 상세 에러 출력
        return JSONResponse(status_code=500, content={"error": str(e)})