from utils.utils import generate
import panel as pn
import asyncio

# always run this first
pn.extension()

# use async callbacks whenever possible
async def callback_fn(contents: str, user: str, instance: pn.chat.ChatInterface):
    message = f"Echoing {user}: {contents}"
    output = ""
    for char in message:
        output += char
        yield output

# this is our chat ui
chat_ui = pn.chat.ChatInterface(
    callback=callback_fn, 
    callback_user="John"
)

# initial greeting
chat_ui.send({"object": "Aloha!", "user": "John", "avatar": "👨🏻‍🍳"}, respond=False)

# layout formation
template = pn.template.MaterialTemplate(title="Simple Chatbot", sidebar=[])
template.main.append(pn.Row(chat_ui))
template.servable()
