from typing import Optional
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/beyoung/v1/8-march")
async def beyoung8march(request: Request):
    data = await request.json()
    print(data)
    return data
