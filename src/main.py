from fastapi import FastAPI

from src.questions.router import router as questions_router

app = FastAPI(title="Test app")
app.include_router(
    questions_router,
)


@app.get("/index")
async def get_root():
    return {
        "msg": "hello",
    }
