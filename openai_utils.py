import logging
from openai import OpenAI

client = OpenAI()
logger = logging.getLogger("uvicorn.error")

OPENAI_URL = "https://api.openai.com/v1/images/generations"


async def generate_text(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.08,
            max_tokens=597,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.critical("Generating text error: %s", e)
        return None


async def generate_image(prompt: str) -> str:
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        logger.info("Generate image response: %s", str(response))
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            return image_url
        else:
            logger.critical("No image was generated or unexpected response format.")
            return None
    except Exception as e:
        logger.critical("Generating image error: %s", e)
        return None
