from contextlib import asynccontextmanager
import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.generate_text import router as gentext_router
from app.services.model_inference import load_qwen_generator

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating new conversation file...")
    conversation_path = Path(__file__).resolve().parent.parent / "conversations" / "main_convo.json"
    conversation_path.parent.mkdir(parents=True, exist_ok=True)
    app.state.conversation_path = conversation_path

    system_message = {
        "role": "system",
        "content": "You are a helpful assistant. Answer concisely, usually in 1-3 short sentences.",
    }

    with open(conversation_path, "w") as file:
        json.dump([system_message], file, indent=2)

    print("Loading text generator...")
    app.state.generator = load_qwen_generator()
    print("Text generator loaded.")

    yield

    print("Deleting text generator...")
    del app.state.generator
    print("Text generator deleted.")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(gentext_router)
