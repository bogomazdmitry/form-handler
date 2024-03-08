from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
import os
import logging
from congratulations.beyoung_8march import generate_congratulation_image, generate_congratulation_text, get_default_congratulation_text

import startup
from telegram_utils import send_telegram_message, send_telegram_photo

load_dotenv()

app = FastAPI()
logger = logging.getLogger('uvicorn.error')

startup.check_env_variables()

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


@app.post("/beyoung/v1/8-march")
async def beyoung_v1_8march(request: Request):
    try:
        data = await request.json()
        if "test" not in request.query_params or not request.query_params["test"]:
            image_url = await generate_congratulation_image(data)
            if image_url is None:
                logger.critical("Image didn't provided")
                raise HTTPException(status_code=500, detail="Internal error")
                
            congratulation_text = await generate_congratulation_text(data)
        else:
            image_url = 'https://cdn.shopclues.com/images/thumbnails/79835/320/320/104787525124666394ID1006929615021796911502242942.jpg'
            congratulation_text = get_default_congratulation_text(data)
            

        await send_telegram_photo(image_url, TELEGRAM_CHAT_ID)
        await send_telegram_message(congratulation_text, TELEGRAM_CHAT_ID)

        return {"message": "Data processed successfully"}
    
    except Exception as e:
        logger.critical("Unexpected error: %s", e)
        raise HTTPException(status_code=500, detail="Internal error")
