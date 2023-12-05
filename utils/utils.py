import random
import json
from utils.common import config, logger
from utils.helper import replace_keywords, transform_dialogue
from openai import OpenAI, AsyncOpenAI

client = OpenAI(api_key=config["OPENAI"]["api_key"])
async_client = AsyncOpenAI(api_key=config["OPENAI"]["api_key"])
DEFAULT_MODEL = "gpt-3.5-turbo"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_memory",
            "description": "Recall content of previous conversation from memory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event": {
                        "type": "string",
                        "description": "Event or topic to recall, e.g. talking about politics, asking someone's status.",
                    },
                    "target": {"type": "string", "description": "person of subject"},
                },
                "required": ["event"],
            },
        },
    }
]


# mock memory retrieval
def get_memory(event: str = "", target: str = ""):
    logger.trace(f"Event: {event}, Target: {target}")
    return "We talked about going to a party."


async def generate2(dialogue: list, memory: str, model: str = DEFAULT_MODEL):
    messages = [
        {
            "role": "system",
            "content": "You are a AI wizard. You speak elegantly and gracefully. Full of wisdom and charm.",
        },
        {
            "role": "user",
            "content": 'The following is a dialogue between you and a friend. \n"""\n{{dialogue}}\n"""\nYou recall your previous conversation, \n"""\n{{memory}}\n"""\nHow do you reply?',
        },
    ]
    mapping = {"{{dialogue}}": str(dialogue), "{{memory}}": memory}
    logger.trace(transform_dialogue(dialogue[1::]))
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
        subject_person = completion.choices[0].message.tool_calls
        logger.trace(subject_person)
        parsed_args = json.loads(subject_person[0].function.arguments)
        memory = get_memory(**parsed_args)
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
            "content": "You are a AI wizard. You speak elegantly and gracefully. Full of wisdom and charm.",
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
    wizard_greetings = [
        "Greetings from the realms beyond!",
        "Well met by moonlight and starshine!",
        "Salutations from the whispers of the ancient winds!",
        "Hail and well met, traveler of the mortal coil!",
        "By the alchemy of old, I bid you welcome!",
        "From the depths of the mystic ether, I greet thee!",
        "May the wisdom of the ages be upon our meeting!",
        "Under the watchful eye of the arcane, our paths cross!",
        "Blessings of the enchanted realms upon you!",
        "In the light of the aurora mystica, greetings!",
    ]
    return random.choice(wizard_greetings)  # default fallback
