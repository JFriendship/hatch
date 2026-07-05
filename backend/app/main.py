from fastapi import FastAPI

from app.api.routes.generate_text import router as gentext_router

app = FastAPI()

app.include_router(gentext_router)