import logging
from http.client import HTTPException
import json
import sys
from fastapi import FastAPI, Request, logger
import httpx
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
app = FastAPI()


required_vars = ["TELEGRAM_BOT_KEY", "TELEGRAM_CHAT_ID", "OPENAI_API_KEY"]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    logger.critical(f"Error: Missing environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

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
    logger.info("Generate image response: " + response)

    if response.data and len(response.data) > 0:
        image_url = response.data[0].url
        return image_url
    else:
        logger.critical("No image was generated or unexpected response format.")
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

async def generate_congratulation(data: dict):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
            {
                "role": "user",
            "content": f"Поздравьте сотрудника от компании Beyoung с 8 Марта, который заполнил форму и получились такие ответы: {json.dumps(data, ensure_ascii=False)}",
            }

            ],
            temperature=1.08,
            max_tokens=597,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.critical(f"Generating text error: {e}")
        return None
    
@app.post("/beyoung/v1/8-march")
async def beyoung8march(request: Request):
    try:
        data = await request.json()

        prompt = f"Сгеннерируй открытку с 8 марта девушке, которая заполнила форму вот с такими данными: {json.dumps(data, ensure_ascii=False)}. не в формате формы "
        logger.info(f"Image prompt: {prompt}")

        image_url = generate_image(prompt)

        congratulation_text = await generate_congratulation(data)
        if congratulation_text == None:
            congratulation_text = f"С 8 Марта, {data["Как тебя зовут?"]}! Вас поздравляет beyoung! Желаем счастья, здоровья и всего наилучшего."
            logger.warn("Congratulation text  created as default text")
        logger.warn(f"Congratulation text: {congratulation_text}")
        await send_telegram_photo(image_url)
        await send_telegram_message(congratulation_text)

        return {"message": "Data processed successfully"}
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
