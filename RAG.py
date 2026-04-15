import gradio as gr 
import html

# =========================================================
# SIMPLE DEMO LOGIC
# Replace mock_reply(message) with ask_question(message) later
# =========================================================
def mock_reply(message):
    q = message.lower().strip()

    if "lesson" in q or "timetable" in q:
        return "Today is Thursday:\n9:00 – 11:00 (Cyber Security)\n12:00 – 14:00 (Digital Forensics)"
    elif "room" in q:
        return "For Cyber Security you are in room HW1/14.\nFor Digital Forensics you are in room OA1/04."
    elif "course" in q:
        return "I can help with course details, modules, entry requirements, and study information."
    elif "it" in q or "support" in q:
        return "You can contact IT Support through the student help desk or the university support portal."
    elif "faq" in q:
        return "I can help with FAQs about enrolment, timetables, support, and student services."
    else:
        return f"I can help with: {message}"


def login_demo(username, password):
    if not username or not password:
        return "Please enter both username and password."
    return "Login demo only. Connect this button to your real authentication system."


# =========================================================
# CHAT RENDERER
# =========================================================
def render_chat(history):
    chat_html = '<div class="chat-wrap">'

    for item in history:
        role = item["role"]
        text = html.escape(item["content"]).replace("\n", "<br>")

        if role == "assistant":
            chat_html += f"""
            <div class="msg-row ai-row">
                <div class="circle ai-circle">AI</div>
                <div class="bubble ai-bubble">{text}</div>
            </div>
            """
        else:
            chat_html += f"""
            <div class="msg-row user-row">
                <div class="user-spacer"></div>
                <div class="bubble user-bubble">{text}</div>
                <div class="circle user-circle">S</div>
            </div>
            """

    chat_html += "</div>"
    return chat_html


def send_message(message, history):
    if not message or not message.strip():
        return history, "", render_chat(history)

    history = history + [{"role": "user", "content": message}]
    reply = mock_reply(message)
    history = history + [{"role": "assistant", "content": reply}]

    return history, "", render_chat(history)


def quick_send(text, history):
    return send_message(text, history)


def add_attachment_notice(history):
    history = history + [
        {"role": "assistant", "content": "Attachment feature placeholder."}
    ]
    return history, render_chat(history)


# =========================================================
# STARTER CHAT
# =========================================================
initial_history = [
    {"role": "assistant", "content": "How may I assist you today?"},
    {"role": "user", "content": "What lessons do I have today?"},
    {
        "role": "assistant",
        "content": "Today is Thursday:\n9:00 – 11:00 (Cyber Security)\n12:00 – 14:00 (Digital Forensics)"
    },
    {"role": "assistant", "content": "What else would you like me to assist you with?"}
]

# =========================================================
# CSS
# =========================================================
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

.panel {
    min-height: 300px;
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
    font-size: 1.05rem !important;
}

.notice-box textarea::placeholder,
.notice-box input::placeholder {
    color: rgba(255,255,255,0.95) !important;
}

.input-box textarea,
.input-box input {
    background: #05b84d !important;
    color: white !important;
    border: 2px solid #214253 !important;
    border-radius: 10px !important;
    font-size: 1rem !important;
    min-height: 48px !important;
}

.input-box textarea::placeholder,
.input-box input::placeholder {
    color: rgba(255,255,255,0.95) !important;
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

.primary-btn button {
    background: #1173b8 !important;
    color: white !important;
    border: 2px solid #183848 !important;
    border-radius: 12px !important;
    min-height: 50px !important;
    font-size: 1.05rem !important;
}

.secondary-btn button,
.quick-btn button,
.arrow-btn button,
.attach-btn button,
.send-btn button {
    border-radius: 12px !important;
    border: 2px solid #214253 !important;
    min-height: 50px !important;
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

.arrow-btn button,
.send-btn button {
    background: #145f82 !important;
    color: white !important;
    min-width: 54px !important;
    font-size: 1.2rem !important;
}

.attach-btn button {
    background: white !important;
    color: black !important;
}

.chat-wrap {
    padding: 6px 0;
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
    max-width: 86%;
    flex: 1;
}

.ai-bubble {
    background: #4ea8d3;
}

.user-bubble {
    background: #05b84d;
}

.chat-panel {
    margin-top: 8px;
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

# =========================================================
# UI
# =========================================================
with gr.Blocks(css=custom_css) as interface:
    chat_state = gr.State(initial_history)

    gr.HTML("""
        <div class="topbar">
            <h1>MyHud</h1>
            <div class="close-btn">✕</div>
        </div>
    """)

    with gr.Column(elem_classes="main-wrap"):

        # -------------------------------------------------
        # TOP AREA
        # -------------------------------------------------
        with gr.Row():
            # LEFT PANEL - LOGIN
            with gr.Column(scale=1, elem_classes="panel"):
                with gr.Row():
                    gr.HTML('<div class="circle ai-circle">AI</div>')
                    login_notice = gr.Textbox(
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
                        username = gr.Textbox(
                            placeholder="Please Enter Username......",
                            show_label=False,
                            elem_classes="input-box"
                        )

                with gr.Row():
                    with gr.Column(scale=1, min_width=120):
                        gr.HTML('<div class="label-chip">Password</div>')
                    with gr.Column(scale=4):
                        password = gr.Textbox(
                            placeholder="Please Enter Password......",
                            type="password",
                            show_label=False,
                            elem_classes="input-box"
                        )

                with gr.Row():
                    gr.HTML("<div></div>")
                    login_btn = gr.Button("Login", elem_classes="primary-btn")

            # RIGHT PANEL - QUICK HELP
            with gr.Column(scale=1, elem_classes="panel"):
                with gr.Row():
                    gr.HTML('<div class="circle ai-circle">AI</div>')
                    gr.Textbox(
                        value="How may I assist you today?",
                        interactive=False,
                        show_label=False,
                        elem_classes="notice-box"
                    )

                with gr.Row():
                    quick_1 = gr.Button("Looking for Timetable information?", elem_classes="quick-btn")
                    gr.Button("➜", elem_classes="arrow-btn")

                with gr.Row():
                    quick_2 = gr.Button("Course Information?", elem_classes="quick-btn")
                    gr.Button("➜", elem_classes="arrow-btn")

                with gr.Row():
                    quick_3 = gr.Button("Contact IT Support", elem_classes="quick-btn")
                    gr.Button("➜", elem_classes="arrow-btn")

                with gr.Row():
                    quick_4 = gr.Button("Click Here For Frequently Asked Questions", elem_classes="quick-btn")
                    gr.Button("➜", elem_classes="arrow-btn")

        # -------------------------------------------------
        # CHAT / DASHBOARD
        # -------------------------------------------------
        with gr.Column(elem_classes="chat-panel"):
            chat_html = gr.HTML(render_chat(initial_history))

            with gr.Row():
                full_tt = gr.Button("See Full Timetable", elem_classes="secondary-btn")
                gr.Button("➜", elem_classes="arrow-btn")

            with gr.Row():
                gr.HTML('<div class="info-tile">Next Lesson: 1hr 30 mins</div>')
                gr.HTML('<div class="info-tile">Assignment Due: 05/03/26</div>')

        # -------------------------------------------------
        # BOTTOM QUERY BAR
        # -------------------------------------------------
        with gr.Row():
            query_box = gr.Textbox(
                placeholder="Please Enter A Query.....",
                show_label=False,
                scale=8,
                elem_classes="query-box"
            )
            attach_btn = gr.Button("Attach", elem_classes="attach-btn", scale=1)
            send_btn = gr.Button("➜", elem_classes="send-btn", scale=1)

    # -------------------------------------------------
    # ACTIONS
    # -------------------------------------------------
    login_btn.click(
        fn=login_demo,
        inputs=[username, password],
        outputs=login_notice
    )

    send_btn.click(
        fn=send_message,
        inputs=[query_box, chat_state],
        outputs=[chat_state, query_box, chat_html]
    )

    query_box.submit(
        fn=send_message,
        inputs=[query_box, chat_state],
        outputs=[chat_state, query_box, chat_html]
    )

    quick_1.click(
        fn=lambda history: quick_send("What lessons do I have today?", history),
        inputs=chat_state,
        outputs=[chat_state, query_box, chat_html]
    )

    quick_2.click(
        fn=lambda history: quick_send("Tell me about course information.", history),
        inputs=chat_state,
        outputs=[chat_state, query_box, chat_html]
    )

    quick_3.click(
        fn=lambda history: quick_send("I need IT support.", history),
        inputs=chat_state,
        outputs=[chat_state, query_box, chat_html]
    )

    quick_4.click(
        fn=lambda history: quick_send("Show me frequently asked questions.", history),
        inputs=chat_state,
        outputs=[chat_state, query_box, chat_html]
    )

    full_tt.click(
        fn=lambda history: quick_send("Show me my full timetable.", history),
        inputs=chat_state,
        outputs=[chat_state, query_box, chat_html]
    )

    attach_btn.click(
        fn=add_attachment_notice,
        inputs=chat_state,
        outputs=[chat_state, chat_html]
    )

interface.launch()