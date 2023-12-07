import random
import json
from utils.common import config, logger
from utils.helper import replace_keywords, transform_dialogue
from utils.vectorize import find_similar, get_metadata
from openai import OpenAI, AsyncOpenAI
from story.extras import SYSTEM_CHARACTER, tools, wizard_greetings

client = OpenAI(api_key=config["OPENAI"]["api_key"])
async_client = AsyncOpenAI(api_key=config["OPENAI"]["api_key"])
DEFAULT_MODEL = "gpt-3.5-turbo"


def activate_recall(func: str, event: str = "", person: str = ""):
    logger.trace(f"Func: {func}, Event: {event}, Target: {person}")
    function_map = {
        "recall_event": (find_similar, [event]),
        "recall_someone": (get_metadata, [person]),
    }
    if func in function_map:
        func, args = function_map[func]
        content_recalled = func(*args)
    else:
        logger.debug("Error: Function is not callable.")
        return ""
    return content_recalled


async def generate2(dialogue: list, memory: str, model: str = DEFAULT_MODEL):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_CHARACTER,
        },
        {
            "role": "user",
            "content": 'The following is a dialogue between you and a friend. \n"""\n{{dialogue}}\n"""\nYou recall previous conversations, \n"""\n{{memory}}\n"""\nHow do you reply?',
        },
    ]
    mapping = {"{{dialogue}}": transform_dialogue(dialogue[1::]), "{{memory}}": memory}
    for message in messages:
        message["content"] = replace_keywords(message["content"], mapping)
    response = await async_client.chat.completions.create(
        model=model, messages=messages, temperature=1
    )
    result = response.choices[0].message.content
    yield result


async def generate(content: str, model: str = DEFAULT_MODEL):
    completion = await async_client.chat.completions.create(
        model=model, messages=content, tools=tools, tool_choice="auto"
    )
    result = completion.choices[0].message.content
    output = ""
    if result:
        for char in result:
            output += char
            yield output
    else:
        tool_calls = completion.choices[0].message.tool_calls
        parsed_args = json.loads(tool_calls[0].function.arguments)
        func_name = tool_calls[0].function.name
        memory = activate_recall(func_name, **parsed_args)
        async for char in generate2(content, memory):
            output = char
            yield output


def summarize(content: str, model: str = DEFAULT_MODEL):
    prompt = [
        {
            "role": "system",
            "content": "You are a helpful historian. You expect to receive a Python list which contains a dialogue between 2 persons, 'assistant' and 'user'. Role 'assistant' represents yourself and role 'user' represents a friend. Your job is to summarize the conversation into a gist. Answer using first-person tone of voice and use 'my friend' to represent the user. Be concise and direct. When the conversation has no meaningful content or a central topic, you reply with a short one-liner.",
        }
    ]
    prompt.append({"role": "user", "content": content})
    # logger.trace(f"{prompt}")
    response = client.chat.completions.create(
        model=model, messages=prompt, temperature=0
    )
    result = response.choices[0].message.content
    return result


def greeting(content: str | None, username: str, model: str = DEFAULT_MODEL):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_CHARACTER,
        },
        {
            "role": "user",
            "content": "You met a long time friend {{friend_name}}. These are the conversation you had previously, \n{{previous_conversation}}\nYou may wonder if your friend is keen to continue the previous topic. Let him know you remember the previous discussion. How would you greet him?",
        },
    ]
    mapping = {"{{friend_name}}": username, "{{previous_conversation}}": content}
    logger.trace(f"Greeting Agent: digesting <<{content}>>")
    if content:
        for message in messages:
            message["content"] = replace_keywords(message["content"], mapping=mapping)
        response = client.chat.completions.create(
            model=model, messages=messages, temperature=1
        )
        result = response.choices[0].message.content
        return result  # greeting generated from LLM
    return random.choice(wizard_greetings)  # default fallback