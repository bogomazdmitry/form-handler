from http.client import HTTPException
import json
from fastapi import FastAPI, Request
import httpx
import os
from openai import OpenAI

client = OpenAI()
app = FastAPI()


CHAT_GPT_KEY = os.getenv("CHAT_GPT_KEY")
TELEGRAM_BOT_KEY = os.getenv("TELEGRAM_BOT_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

OPENAI_URL = "https://api.openai.com/v1/images/generations"
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_KEY}"


def generate_image(prompt: str):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    print(response)
    if response.data and len(response.data) > 0:
        image_url = response.data[0].url  # Adjusted to use attribute access
        return image_url
    else:
        # Handle case where no image is generated or response is unexpected
        print("No image was generated or unexpected response format.")
        return None


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
    try:
        data = await request.json()

        prompt = "Сгеннерируй открытку с 8 марта девушке, которая заполнила форму вот с такими данными: " + json.dumps(data, ensure_ascii=False) + ". не в формате формы "
        print(prompt)

        image_url = generate_image(prompt)
        await send_telegram_photo(image_url)

        congratulation_text = "С 8 Марта, " + data["Как тебя зовут?"] + "! Вас поздравляет beyoung! Желаем счастья, здоровья и всего наилучшего."
        await send_telegram_message(congratulation_text)

        return {"message": "Data processed successfully"}
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
