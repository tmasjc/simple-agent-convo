from utils.common import config, logger
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=config["OPENAI"]["api_key"])

async def generate(content: str, model: str = "gpt-3.5-turbo"):
    completion = await client.chat.completions.create(
        model=model, messages=content
    )
    result = completion.choices[0].message.content
    output = ""
    for char in result:
        output += char
        yield output
