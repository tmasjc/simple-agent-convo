from utils.utils import generate
from utils.common import logger, redis_client
import panel as pn
from bokeh.io import curdoc
import json

# initialize and configure Panel
pn.extension("perspective")

# get session id as convo marker
doc = curdoc()
CONVERSATION_ID = doc.session_context.id
logger.trace(f"Start new: {CONVERSATION_ID}")

# update system prompt here
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

async def chat_fn(content: str, user: str, instance: pn.chat.ChatInterface):
    messages.append({"role": "user", "content": content})
    
    # stream output to screen
    final_output = ""
    async for partial_result in generate(messages):
        final_output = partial_result
        yield partial_result
    
    # append and log output when finish
    messages.append({"role": "assistant", "content": final_output})
    redis_client.set(CONVERSATION_ID, json.dumps(messages))
    logger.trace(messages)

# build chat function
chat_ui = pn.chat.ChatInterface(
    callback=chat_fn, 
    callback_user="Bot",
    message_params=dict(
        default_avatars={
            "Assistant": "🤖", 
            "User": "🧔🏻‍♂️"
        },
    )
)

# initial greeting
chat_ui.send({"object": "Aloha!", "user": "Bot"}, respond=False)

# layout formation
template = pn.template.MaterialTemplate(title="Simple Chatbot", sidebar=[])
template.main.append(pn.Row(chat_ui))
template.servable()
