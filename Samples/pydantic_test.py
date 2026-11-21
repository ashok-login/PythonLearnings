from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class RequestData(BaseModel):
    prompt: str
    max_new_tokens: int = Field(default=200, gt=0, le=500)

@app.post("/generate")
def generate_text(data: RequestData) -> dict[str, str | int]:
    return {
        "received_prompt": data.prompt,
        "token_limit": data.max_new_tokens,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
