import json
import logging
from openai_utils import generate_image, generate_text

logger = logging.getLogger('uvicorn.error')


async def generate_congratulation_text(data: dict) -> str:
    congratulation_text = await generate_text(f"Поздравьте сотрудника от компании Beyoung с 8 Марта, который заполнил форму и получились такие ответы: {json.dumps(data, ensure_ascii=False)}")
    if congratulation_text is not None:
        return congratulation_text
    logger.warning("Congratulation text created as default text")
    return get_default_congratulation_text(data)

def get_default_congratulation_text(data: dict) -> str:
    if "Как тебя зовут?" in data:
        name = data["Как тебя зовут?"]
        congratulation_text = f"С 8 Марта, {name}! Вас поздравляет beyoung! Желаем счастья, здоровья и всего наилучшего."
    else:
        congratulation_text = "С 8 Марта! Вас поздравляет beyoung! Желаем счастья, здоровья и всего наилучшего."

    return congratulation_text


async def generate_congratulation_image(data: dict) -> str:
    prompt = f"Сгеннерируй открытку с 8 марта девушке, которая заполнила форму вот с такими данными: {json.dumps(data, ensure_ascii=False)}. не в формате формы"
    logger.info("Image prompt: %s", prompt)
    return await generate_image(prompt)
