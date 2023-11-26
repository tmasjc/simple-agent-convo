from utils.common import config, logger
from openai import OpenAI, AsyncOpenAI

client = OpenAI(api_key=config["OPENAI"]["api_key"])
async_client = AsyncOpenAI(api_key=config["OPENAI"]["api_key"])
DEFAULT_MODEL = "gpt-3.5-turbo"


async def generate(content: str, model: str = DEFAULT_MODEL):
    completion = await async_client.chat.completions.create(model=model, messages=content)
    result = completion.choices[0].message.content
    output = ""
    for char in result:
        output += char
        yield output


def summarize(content: str, model: str = DEFAULT_MODEL):
    prompt = [
        {
            "role": "system",
            "content": "Your job is to summarize a conversation like a professional. You expect to receive a Python list. It contains a dialogue between 2 persons, 'assistant' and 'user'. Role `assistant` represents yourself and role `user` represents a friend. Please summarize the conversation into a gist. Answer using first-person tone of voice and use 'my friend' to represent the user. Be concise and direct.",
        }
    ]
    prompt.append({"role": "user", "content": content})
    # logger.trace(f"{prompt}")
    response = client.chat.completions.create(model=model, messages=prompt, temperature=0)
    result   = response.choices[0].message.content
    return result
