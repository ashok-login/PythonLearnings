import os
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
from fastapi import FastAPI
from pydantic import BaseModel
import torch

load_dotenv()  # Load environment variables from .env file

hf_token = os.getenv("HF_CUSTOM_TOKEN")

if not hf_token:
    raise ValueError("HF_CUSTOM_TOKEN is missing. Check your .env file.")

login(token=hf_token)

model_name: str = os.getenv("MODEL_NAME", "gpt2")
cache_dir = os.getenv("HF_CACHE_DIR", None)

tokenizer = AutoTokenizer.from_pretrained(model_name,
                                          cache_dir=cache_dir,
                                          token=hf_token,
                                          trust_remote_code=True)
if not torch.cuda.is_available():
    raise RuntimeError("""CUDA is not available. Please ensure you have """
                       """a compatible GPU and the necessary drivers installed.""")
device = torch.device("cuda:0")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir=cache_dir,
    token=hf_token,
    trust_remote_code=True).to(device)

model.eval()  # Set the model to evaluation mode

print(f"Model device: {next(model.parameters()).device}")

# import torch
app = FastAPI()

class RequestData(BaseModel):
    prompt: str
    max_new_tokens: int = 200

@app.post("/generate")
def generate_text(data: RequestData):
    inputs = tokenizer(
        data.prompt,
        return_tensors="pt"
        ).to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=data.max_new_tokens
            )
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Generated text: {result}")
    return {"generated_text": result}

@app.get("/")
def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
