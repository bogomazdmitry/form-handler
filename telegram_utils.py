import os

import httpx

TELEGRAM_BOT_KEY = os.getenv("TELEGRAM_BOT_KEY")
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_KEY}"

async def send_telegram_message(text: str, chat_id: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{TELEGRAM_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text}
        )


async def send_telegram_photo(photo_url: str, chat_id: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{TELEGRAM_URL}/sendPhoto",
            json={"chat_id": chat_id, "photo": photo_url}
        )
