import gradio as gr

custom_css = """
body, .gradio-container {
    background: #e7e7e7 !important;
    font-family: "Segoe UI", Arial, sans-serif;
}

.gradio-container {
    max-width: 640px !important;
    margin: 0 auto !important;
    padding: 0 !important;
}

footer {
    display: none !important;
}

.topbar {
    background: #145f82;
    color: white;
    padding: 16px 20px;
    border: 2px solid #0d445b;
    border-bottom: 2px solid #0d445b;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.topbar h1 {
    margin: 0;
    font-size: 1.9rem;
    font-weight: 500;
}

.close-btn {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    background: #ff1b1b;
    color: white;
    border: 2px solid #0d445b;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    font-weight: bold;
}

.main-wrap {
    padding: 18px 12px 0 12px;
    min-height: 620px;
    box-sizing: border-box;
    border-left: 2px solid #145f82;
    border-right: 2px solid #145f82;
}

.chat-area {
    min-height: 540px;
}

.msg-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 18px;
}

.user-row {
    justify-content: flex-end;
}

.circle {
    width: 54px;
    height: 54px;
    min-width: 54px;
    border-radius: 50%;
    border: 2px solid #183848;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1rem;
    box-sizing: border-box;
}

.ai-circle {
    background: #0b79c7;
}

.user-circle {
    background: #00B050;
}

.user-spacer {
    width: 54px;
    min-width: 54px;
}

.bubble {
    border: 2px solid #214253;
    border-radius: 12px;
    padding: 14px 16px;
    color: white;
    font-size: 1rem;
    line-height: 1.35;
    box-sizing: border-box;
    flex: 1;
}

.ai-bubble {
    background: #4ea8d3;
}

.user-bubble {
    background: #00B050;
}

.bottom-bar {
    border-left: 2px solid #145f82;
    border-right: 2px solid #145f82;
    border-top: 2px solid #145f82;
    border-bottom: 2px solid #145f82;
    padding: 0;
}

.query-box textarea,
.query-box input {
    border: none !important;
    border-radius: 0 !important;
    min-height: 48px !important;
    font-size: 1rem !important;
    box-shadow: none !important;
    background: white !important;
}

.send-btn button {
    background: white !important;
    color: #145f82 !important;
    border: none !important;
    border-radius: 0 !important;
    min-height: 48px !important;
    min-width: 60px !important;
    font-size: 1.5rem !important;
    box-shadow: none !important;
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.HTML("""
        <div class="topbar">
            <h1>MyHud AI Chatbot</h1>
            <div class="close-btn">✕</div>
        </div>
    """)

    with gr.Column(elem_classes="main-wrap"):
        with gr.Column(elem_classes="chat-area"):
            gr.HTML("""
                <div class="msg-row">
                    <div class="circle ai-circle">AI</div>
                    <div class="bubble ai-bubble">How may I assist you today?</div>
                </div>
            """)

    with gr.Row(elem_classes="bottom-bar"):
        gr.Textbox(
            placeholder="Please Enter A Query....",
            show_label=False,
            scale=9,
            elem_classes="query-box"
        )
        gr.Button("➜", elem_classes="send-btn", scale=1)

demo.launch()