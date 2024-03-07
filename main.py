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

openai.api_key = CHAT_GPT_KEY

async def generate_image(prompt: str):

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
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
    try:
        data = await request.json()

        image_response = await generate_image("Сгеннерируй поздравление-открытку с 8 марта девушке, которая заполнила форму вот с такими данными: " 
                                              + json.dumps(data))

        if 'data' in image_response and len(image_response['data']) > 0 and 'url' in image_response['data'][0]:
            image_url = image_response['data'][0]['url']
        else:
            print("Некорректный формат ответа от API:", image_response)
            raise HTTPException(status_code=500, detail="Ошибка при обработке ответа от API")

        await send_telegram_photo(image_url)

        congratulation_text = "С 8 Марта, " + data["Как тебя зовут?"] + "! Вас поздравляет beyoung! Желаем счастья, здоровья и всего наилучшего."
        await send_telegram_message(congratulation_text)

        return {"message": "Data processed successfully"}
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")



async def beyoung8march(request: Request):
    try:
        data = await request.json()
        image_response = await generate_image(data['prompt'])
        
        if 'data' in image_response and len(image_response['data']) > 0 and 'url' in image_response['data'][0]:
            image_url = image_response['data'][0]['url']
        else:
            # Если структура ответа не соответствует ожидаемой, логируем и возвращаем ошибку
            print("Некорректный формат ответа от API:", image_response)
            raise HTTPException(status_code=500, detail="Ошибка при обработке ответа от API")

        # Отправка сгенерированного изображения и текста поздравления в Telegram
        await send_telegram_photo(image_url)
        congratulation_text = "С 8 Марта! Желаем счастья, здоровья и всего наилучшего."
        await send_telegram_message(congratulation_text)

        return {"message": "Data processed successfully"}
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
