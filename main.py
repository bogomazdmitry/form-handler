from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/beyoung/v1/8-march")
def beyoung8march(data):
    print(data)
    return data