import json
import panel as pn
from bokeh.io import curdoc
from utils.utils import generate
from utils.common import logger, redis_client
from utils.database import ChatSession, add_session_record
from mock.mock_data import mock_session

# initialize and configure Panel
pn.extension("perspective")

# to get current panel document object
doc = curdoc()

# conversation entities
BOT  = mock_session["bot"].get("name", "bot")
USER = mock_session["user"].get("name", "user")

CURRENT_SESSION = ChatSession(
    chat_session_id=doc.session_context.id, 
    bot_identifier=BOT, 
    player_identifier=USER
    )
logger.trace(f"{CURRENT_SESSION}")

# update system prompt here
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

# chat's callback func
async def chat_fn(content: str, user: str, instance: pn.chat.ChatInterface):
    # only do once at the beginning
    if len(messages) == 1:
        add_session_record(CURRENT_SESSION)
        logger.success("Successfuly inserted new record.")

    # stream output to screen
    final_output = ""
    messages.append({"role": "user", "content": content})
    async for partial_result in generate(messages):
        final_output = partial_result
        yield partial_result

    # append and log output when finish
    messages.append({"role": "assistant", "content": final_output})
    redis_client.set(doc.session_context.id, json.dumps(messages))
    # logger.trace(messages)
    logger.trace("Messages++")

chat_ui = pn.chat.ChatInterface(
    callback=chat_fn,
    callback_user=BOT,
    message_params=dict(
        default_avatars={
            BOT:  mock_session["bot"]["avatar"],
            USER: mock_session["user"]["avatar"],
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