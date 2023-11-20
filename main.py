from utils.utils import generate
import gradio as gr

def chat_with_openai(message, history):
    return generate(message)

gr.ChatInterface(chat_with_openai).launch()