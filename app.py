import json
import panel as pn
from bokeh.io import curdoc
from utils.common import logger, redis_client
from utils.utils import generate, greeting
from utils.database import ChatSession, add_session_record
from utils.memory import retrieve_latest_memory
from utils.vectorize import initiate_vector
from mock.mock_data import mock_session
from story.extras import SYSTEM_CHARACTER

# break if Redis isn't up
try:
    redis_client.ping()
    print("Connected to Redis")
except Exception as e:
    logger.debug("Check Redis")
    exit(1)

# initialize and configure Panel
pn.extension()

# to get current panel document object
doc = curdoc()
SESSION_ID = doc.session_context.id

# conversation entities
BOT = mock_session["bot"].get("name", "bot")
USER = pn.state.user
logger.success(f"New logged in: {pn.state.user}")

CURRENT_SESSION = ChatSession(
    chat_session_id=SESSION_ID, bot_identifier=BOT, player_identifier=USER
)
logger.trace(f"{CURRENT_SESSION}")

# update system prompt here
messages = [
    {
        "role": "system",
        "content": SYSTEM_CHARACTER,
    },
]


# chat's callback func
async def chat_fn(content: str, user: str, instance: pn.chat.ChatInterface):
    # only do once at the beginning
    if len(messages) == 1:
        add_session_record(CURRENT_SESSION)  # for memory database
        initiate_vector(session_id=SESSION_ID, user=USER)  # for vector database
        logger.success("Began conversation. Added new record.")

    # stream output to screen
    final_output = ""
    messages.append({"role": "user", "content": content})
    async for partial_result in generate(user, messages):
        final_output = partial_result
        yield partial_result

    # append and log output when finish
    messages.append({"role": "assistant", "content": final_output})
    redis_client.set(SESSION_ID, json.dumps(messages))
    # logger.trace(messages)
    logger.trace("Messages++")


chat_ui = pn.chat.ChatInterface(
    callback=chat_fn,
    callback_user=BOT,
    message_params=dict(
        default_avatars={BOT: mock_session["bot"]["avatar"]},
    ),
)
pn.chat.ChatInterface.user = USER

# initial greeting func
if USER:
    memory = retrieve_latest_memory("player_identifier", USER)
    chat_ui.send({"object": greeting(memory, USER), "user": BOT}, respond=False)

# logout button
logout = pn.widgets.Button(icon="logout", name="Exit Chat")
logout.js_on_click(code="""window.location.href = './logout'""")

template = pn.template.BootstrapTemplate(
    title="Wizard Bob", sidebar=[], header_background="#2F4F4F "
)
template.header.append(logout)
template.main.append(pn.Column(chat_ui))
template.servable()
