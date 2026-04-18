import gradio as gr

custom_css = """
body, .gradio-container {
    background: #e7e7e7 !important;
    font-family: "Segoe UI", Arial, sans-serif;
}

.gradio-container {
    max-width: 650px !important;
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
    border-bottom: 2px solid #0d445b;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.topbar h1 {
    margin: 0;
    font-size: 2rem;
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
    font-size: 1.35rem;
    font-weight: bold;
}

.main-wrap {
    padding: 14px;
}

.chat-area {
    min-height: 460px;
    margin-top: 8px;
}

.msg-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 16px;
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
}

.ai-circle {
    background: #0b79c7;
}

.user-circle {
    background: #05b84d;
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
    line-height: 1.4;
    box-sizing: border-box;
    flex: 1;
}

.ai-bubble {
    background: #4ea8d3;
}

.user-bubble {
    background: #05b84d;
}

.info-tile {
    background: #145f82;
    color: white;
    border: 2px solid #0d445b;
    border-radius: 12px;
    padding: 16px;
    font-size: 1.05rem;
    text-align: center;
    font-weight: 500;
}

.query-box textarea,
.query-box input {
    border: 2px solid #214253 !important;
    border-radius: 0 !important;
    min-height: 48px !important;
    font-size: 1rem !important;
}

.send-btn button {
    background: #145f82 !important;
    color: white !important;
    border: 2px solid #214253 !important;
    border-radius: 0 !important;
    min-height: 48px !important;
    min-width: 60px !important;
    font-size: 1.2rem !important;
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.HTML("""
        <div class="topbar">
            <h1>MyHud</h1>
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

                <div class="msg-row user-row">
                    <div class="user-spacer"></div>
                    <div class="bubble user-bubble">Which rooms are my lessons in?</div>
                    <div class="circle user-circle">S</div>
                </div>

                <div class="msg-row">
                    <div class="circle ai-circle">AI</div>
                    <div class="bubble ai-bubble">
                        For Cyber Security you are in room HW1/14<br>
                        For Digital Forensics you are in room OA1/04
                    </div>
                </div>

                <div class="msg-row">
                    <div class="circle ai-circle">AI</div>
                    <div class="bubble ai-bubble">Is there anything else I can assist you with?</div>
                </div>
            """)

        with gr.Row():
            gr.HTML('<div class="info-tile">Next Lesson: 1hr 30 mins</div>')
            gr.HTML('<div class="info-tile">Assignment Due: 05/03/26</div>')

        with gr.Row():
            gr.Textbox(
                placeholder="Please Enter A Query.....",
                show_label=False,
                scale=8,
                elem_classes="query-box"
            )
            gr.Button("➜", elem_classes="send-btn", scale=1)

demo.launch()