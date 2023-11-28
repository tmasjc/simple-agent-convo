from utils.common import config, logger
from openai import OpenAI, AsyncOpenAI

client = OpenAI(api_key=config["OPENAI"]["api_key"])
async_client = AsyncOpenAI(api_key=config["OPENAI"]["api_key"])
DEFAULT_MODEL = "gpt-3.5-turbo"


async def generate(content: str, model: str = DEFAULT_MODEL):
    completion = await async_client.chat.completions.create(
        model=model, messages=content
    )
    result = completion.choices[0].message.content
    output = ""
    for char in result:
        output += char
        yield output


def summarize(content: str, model: str = DEFAULT_MODEL):
    prompt = [
        {
        "role": "system",
        "content": "You are a helpful historian. You expect to receive a Python list which contains a dialogue between 2 persons, 'assistant' and 'user'. Role 'assistant' represents yourself and role 'user' represents a friend. Your job is to summarize the conversation into a gist. Answer using first-person tone of voice and use 'my friend' to represent the user. Be concise and direct. When the conversation has no meaningful content or a central topic, you reply with a short one-liner."
        }
    ]
    prompt.append({"role": "user", "content": content})
    # logger.trace(f"{prompt}")
    response = client.chat.completions.create(
        model=model, messages=prompt, temperature=0
    )
    result = response.choices[0].message.content
    return result


def greeting(content: str, model: str = DEFAULT_MODEL):
    messages = [
        {
            "role": "system",
            "content": "You are a AI wizard. You speak elegantly and gracefully. Full of wisdom and charm.",
        },
        {
            "role": "user",
            "content": "You met a long time friend. These are the conversation you had previously, \n\n{{previous_conversation}}\n\nYou may wonder if your friend is keen to continue the previous topic. Let him know you remember the previous discussion. How would you greet him?",
        },
    ]
    logger.trace(f"Greeting Agent: digesting <<{content}>>")
    if content:
        for message in messages:
            if "{{previous_conversation}}" in message["content"]:
                message["content"] = message["content"].replace(
                    "{{previous_conversation}}", content
                )
        response = client.chat.completions.create(
            model=model, messages=messages, temperature=1
        )
        result = response.choices[0].message.content
        return result
    return "Greetings!" # default fallback