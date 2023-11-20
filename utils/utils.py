from utils.common import config, logger
from openai import OpenAI

client = OpenAI(
    api_key=config['OPENAI']['api_key']
)

messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

def generate(user_messsage: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Chat completion via OpenAI API.

    Args:
    - prompt: The text prompt to send.
    - model: Which model to use.

    Returns:
    - str: Text result from OpenAI model.
    """
    messages.append({"role": "user", "content": user_messsage})
    completion = client.chat.completions.create(model=model, messages=messages)
    reply = completion.choices[0].message.content
    messages.append({"role": "user", "content": reply})
    logger.trace(messages)
    return reply
