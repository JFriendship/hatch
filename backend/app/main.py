from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.generate_text import router as gentext_router
from app.services.model_inference import load_qwen_generator

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading text generator...")
    app.state.generator = load_qwen_generator()

    yield

    print("Deleting text generator...")
    del app.state.generator

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(gentext_router)