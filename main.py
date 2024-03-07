import json
from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

CHAT_GPT_KEY = os.getenv("CHAT_GPT_KEY")
TELEGRAM_BOT_KEY = os.getenv("TELEGRAM_BOT_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

OPENAI_URL = "https://api.openai.com/v1/images/generations"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_KEY}"

async def generate_image(prompt: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            OPENAI_URL,
            headers={"Authorization": f"Bearer {CHAT_GPT_KEY}"},
            json={"prompt": prompt, "n": 1, "size": "1024x1024"}
        )
    return response.json()

async def send_telegram_message(text: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{TELEGRAM_URL}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text}
        )

async def send_telegram_photo(photo_url: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{TELEGRAM_URL}/sendPhoto",
            json={"chat_id": TELEGRAM_CHAT_ID, "photo": photo_url}
        )

@app.post("/beyoung/v1/8-march")
async def beyoung8march(request: Request):
    data = await request.json()

    # image_response = await generate_image("Сгеннерируй поздравление-открытку с 8 марта девушке, которая заполнила форму вот с такими данными: " 
    #                                       + json.dumps(data))
    # image_url = image_response['data'][0]['url']

    await send_telegram_photo("https://www.google.ru/url?sa=i&url=https%3A%2F%2Fsitechecker.pro%2Fwhat-is-422-status-code%2F&psig=AOvVaw2jIJ7uMazcVUkiyNzfpWuz&ust=1709927627043000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCMit7ff24oQDFQAAAAAdAAAAABAE")

    congratulation_text = "С 8 Марта, " + data["Как тебя зовут?"] + "! Желаем счастья, здоровья и всего наилучшего."
    await send_telegram_message(congratulation_text)

    return {"message": "Data processed successfully"}
