import gradio as gr

custom_css = """
body, .gradio-container {
    background: #e7e7e7 !important;
    font-family: "Segoe UI", Arial, sans-serif;
}

.gradio-container {
    max-width: 1280px !important;
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
    padding: 16px;
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

.notice-box textarea,
.notice-box input {
    background: #4ea8d3 !important;
    color: white !important;
    border: 2px solid #214253 !important;
    border-radius: 12px !important;
}

.notice-box textarea::placeholder,
.notice-box input::placeholder,
.input-box textarea::placeholder,
.input-box input::placeholder {
    color: rgba(255,255,255,0.95) !important;
}

.input-box textarea,
.input-box input {
    background: #05b84d !important;
    color: white !important;
    border: 2px solid #214253 !important;
    border-radius: 10px !important;
    min-height: 48px !important;
}

.label-chip {
    background: #05b84d;
    color: white;
    border: 2px solid #214253;
    border-radius: 10px;
    padding: 12px 14px;
    text-align: center;
    font-size: 1rem;
    font-weight: 500;
}

.primary-btn button,
.secondary-btn button,
.quick-btn button,
.arrow-btn button,
.send-btn button {
    border-radius: 12px !important;
    border: 2px solid #214253 !important;
    min-height: 50px !important;
}

.primary-btn button,
.arrow-btn button,
.send-btn button {
    background: #145f82 !important;
    color: white !important;
}

.secondary-btn button,
.quick-btn button {
    background: #4ea8d3 !important;
    color: white !important;
}

.quick-btn button {
    min-height: 56px !important;
    justify-content: flex-start !important;
    text-align: left !important;
    font-size: 1rem !important;
}

.chat-area {
    margin-top: 8px;
}

.msg-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 14px;
}

.user-row {
    justify-content: flex-end;
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
    max-width: 86%;
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
    border-radius: 10px !important;
    min-height: 46px !important;
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

        # Top section
        with gr.Row():
            # Left side
            with gr.Column(scale=1):
                with gr.Row():
                    gr.HTML('<div class="circle ai-circle">AI</div>')
                    gr.Textbox(
                        value="To Access all Features Please Login.",
                        interactive=False,
                        show_label=False,
                        elem_classes="notice-box"
                    )

                with gr.Row():
                    gr.Button("Language", elem_classes="secondary-btn")
                    gr.Button("➜", elem_classes="arrow-btn")
                    gr.Button("Accessibility", elem_classes="secondary-btn")
                    gr.Button("➜", elem_classes="arrow-btn")

                with gr.Row():
                    with gr.Column(scale=1, min_width=120):
                        gr.HTML('<div class="label-chip">Username</div>')
                    with gr.Column(scale=4):
                        gr.Textbox(
                            placeholder="Please Enter Username......",
                            show_label=False,
                            elem_classes="input-box"
                        )

                with gr.Row():
                    with gr.Column(scale=1, min_width=120):
                        gr.HTML('<div class="label-chip">Password</div>')
                    with gr.Column(scale=4):
                        gr.Textbox(
                            placeholder="Please Enter Password......",
                            type="password",
                            show_label=False,
                            elem_classes="input-box"
                        )

                with gr.Row():
                    gr.HTML("<div></div>")
                    gr.Button("Login", elem_classes="primary-btn")

            # Right side
            with gr.Column(scale=1):
                with gr.Row():
                    gr.HTML('<div class="circle ai-circle">AI</div>')
                    gr.Textbox(
                        value="How may I assist you today?",
                        interactive=False,
                        show_label=False,
                        elem_classes="notice-box"
                    )

                with gr.Row():
                    gr.Button("Looking for Timetable information?", elem_classes="quick-btn")
                    gr.Button("➜", elem_classes="arrow-btn")

                with gr.Row():
                    gr.Button("Course Information?", elem_classes="quick-btn")
                    gr.Button("➜", elem_classes="arrow-btn")

                with gr.Row():
                    gr.Button("Contact IT Support", elem_classes="quick-btn")
                    gr.Button("➜", elem_classes="arrow-btn")

                with gr.Row():
                    gr.Button("Click Here For Frequently Asked Questions", elem_classes="quick-btn")
                    gr.Button("➜", elem_classes="arrow-btn")

        # Chat preview
        with gr.Column(elem_classes="chat-area"):
            gr.HTML("""
                <div class="msg-row">
                    <div class="circle ai-circle">AI</div>
                    <div class="bubble ai-bubble">How may I assist you today?</div>
                </div>

                <div class="msg-row user-row">
                    <div class="user-spacer"></div>
                    <div class="bubble user-bubble">What lessons do I have today?</div>
                    <div class="circle user-circle">S</div>
                </div>

                <div class="msg-row">
                    <div class="circle ai-circle">AI</div>
                    <div class="bubble ai-bubble">
                        Today is Thursday:<br>
                        9:00 – 11:00 (Cyber Security)<br>
                        12:00 – 14:00 (Digital Forensics)
                    </div>
                </div>

                <div class="msg-row">
                    <div style="width:54px;"></div>
                    <div style="display:flex; gap:12px; width:100%; max-width:420px;">
                        <button style="
                            background:#4ea8d3;
                            color:white;
                            border:2px solid #214253;
                            border-radius:12px;
                            min-height:50px;
                            padding:0 18px;
                            font-size:1rem;
                            cursor:pointer;
                        ">See Full Timetable</button>

                        <button style="
                            background:#145f82;
                            color:white;
                            border:2px solid #214253;
                            border-radius:12px;
                            min-height:50px;
                            min-width:54px;
                            font-size:1.2rem;
                            cursor:pointer;
                        ">➜</button>
                    </div>
                </div>

                <div class="msg-row">
                    <div class="circle ai-circle">AI</div>
                    <div class="bubble ai-bubble">What else would you like me to assist you with?</div>
                </div>
            """)

        with gr.Row():
            gr.HTML('<div class="info-tile">Next Lesson: 1hr 30 mins</div>')
            gr.HTML('<div class="info-tile">Assignment Due: 05/03/26</div>')

        # Bottom query bar
        with gr.Row():
            gr.Textbox(
                placeholder="Please Enter A Query.....",
                show_label=False,
                scale=8,
                elem_classes="query-box"
            )
            gr.Button("➜", elem_classes="send-btn", scale=1)

demo.launch()