from utils.utils import generate
from utils.common import logger, redis_client
import panel as pn
from bokeh.io import curdoc
import json

# initialize and configure Panel
pn.extension("perspective")

# conversation session info
doc = curdoc()
chat_session = {
    "id": doc.session_context.id,
    "bot":  {"name": "Bob", "avatar": "🤖"},
    "user": {"name": "Tom", "avatar": "👨🏻"},
}
logger.trace(f"Start new: {chat_session}")

# update system prompt here
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

# chat's callback func
async def chat_fn(content: str, user: str, instance: pn.chat.ChatInterface):
    messages.append({"role": "user", "content": content})

    # stream output to screen
    final_output = ""
    async for partial_result in generate(messages):
        final_output = partial_result
        yield partial_result

    # append and log output when finish
    messages.append({"role": "assistant", "content": final_output})
    redis_client.set(chat_session.get("id"), json.dumps(messages))
    logger.trace(messages)


# build chat function
BOT  = chat_session["bot"].get("name", "bot")
USER = chat_session["user"].get("name", "user")

chat_ui = pn.chat.ChatInterface(
    callback=chat_fn,
    callback_user=BOT,
    message_params=dict(
        default_avatars={
            BOT:  chat_session["bot"]["avatar"],
            USER: chat_session["user"]["avatar"],
        },
    ),
)
pn.chat.ChatInterface.user = USER

# initial greeting
chat_ui.send(
    {"object": "Aloha!", "user": BOT}, respond=False
)

# layout formation
template = pn.template.MaterialTemplate(title="Simple Chatbot", sidebar=[])
template.main.append(pn.Row(chat_ui))
template.servable()
