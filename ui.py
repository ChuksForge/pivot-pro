# ui.py
import gradio as gr
from pivot_pro import coach

conversation_history = []

def chat(user_input, history):
    global conversation_history

    if not user_input.strip():
        return "", history

    # Get response using Anthropic-format history
    reply = coach(user_input, conversation_history)

    # Gradio 6.x format
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": reply})

    return "", history

def reset():
    global conversation_history
    conversation_history = []
    return "", []

with gr.Blocks(title="PivotPro") as demo:
    gr.Markdown("# 🎯 PivotPro\n### Direct, strategic career pivot coaching.")
    gr.Markdown("Tell me where you are and where you want to go. I'll tell you exactly how to get there.")

    chatbot = gr.Chatbot(height=550, show_label=False)

    msg = gr.Textbox(
        placeholder="Tell me about your current role and what you're thinking of moving into...",
        label="Your message",
        lines=3
    )
    with gr.Row():
        submit = gr.Button("Send →", variant="primary")
        clear = gr.Button("New Session")

    submit.click(chat, [msg, chatbot], [msg, chatbot])
    msg.submit(chat, [msg, chatbot], [msg, chatbot])
    clear.click(reset, outputs=[msg, chatbot])

demo.launch(theme=gr.themes.Soft())