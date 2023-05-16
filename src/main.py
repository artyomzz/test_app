from fastapi import FastAPI

app = FastAPI()


@app.get("/index")
async def get_root():
    return {
        "msg": "hello",
    }
