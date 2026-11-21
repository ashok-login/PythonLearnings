import gradio as gr
import requests

API_URL = "http://localhost:8000/generate"  # Endpoint for text generation
#API2_URL = "http://localhost:90/geminiask"

def chat_fn(message: str, history: list):
    try:
        prmp = f"you are a helpful assistant. {message}"
        resp = requests.post(API_URL, json={"prompt": prmp})
        if resp.status_code == 200:
            return resp.json()["generated_text"]
        return f"Error {resp.status_code}: {resp.text}"
    except Exception as e:
        return f"API Error: {str(e)}"

gr.ChatInterface(
    fn=chat_fn,
    title="Locally deployed Chatbot"
).launch(server_name="0.0.0.0", server_port=8989,share=False)
