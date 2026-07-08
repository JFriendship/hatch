from contextlib import asynccontextmanager
from fastapi import FastAPI

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

app.include_router(gentext_router)