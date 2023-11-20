from utils.utils import generate
import gradio as gr

def chat_with_openai(message, history):
    return generate(message)

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg     = gr.Textbox(lines=1)
    clear   = gr.ClearButton([msg, chatbot])

    def greetings():
        bot_message = "Aloha"
        return bot_message

    def respond(message, chat_history):
        if chat_history is None:
            return "", "greetings"
        else:
            bot_message = generate(message)
            chat_history.append((message, bot_message))
            return "", chat_history
    
    # event trigger
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch()