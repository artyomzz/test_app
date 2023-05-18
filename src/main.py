from fastapi import FastAPI

from src.audio_service.router import router as records_router
from src.questions.router import router as questions_router

app = FastAPI(title="Test app")
app.include_router(
    questions_router,
)
app.include_router(
    records_router,
)
