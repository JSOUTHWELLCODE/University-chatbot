#import ollama
import re
import gradio as gr
#from concurrent.futures import ThreadPoolExecutor

'''
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.config import Settings
from chromadb import Client, chromadb
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM, OllamaEmbeddings
import os
from VectorStore import returnDB
from Fuzzymatching import Fuzzymatch
'''

'''
matcher = Fuzzymatch("/Users/Jonny/Desktop/University-chatbot/Contact emails/CONTACT EMAILS.xlsx")

path = "/Users/Jonny/Desktop/University-chatbot/PDF faqs/FAQS clearing.pdf")
persist_path = "/Users/Jonny/Desktop/University-chatbot/PDF faqs/University_Knowledge_Base"

embedding_function = OllamaEmbeddings(model="deepseek-r1:1.5b")
llm = OllamaLLM(model="deepseek-r1:1.5b")

vector_db = returnDB(embedding_function, persist_path)
retriever = vector_db.as_retriever()

def query_deepseek(question, context):
    prompt = (
        "You are a University Assistant at the university of Huddersfield. Use the provided Context to answer the Question. "
        "If the Question is just a greeting (like 'Hello' or 'Hi'), just say 'Hello! How can I help you with the information about the university?' "
        "Otherwise, use the context provided below.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}"
    )

    response = llm.invoke(prompt)
    final_answer = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
    return final_answer

def retrieve_context(question):
    results = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in results])
    return context

def ask_question(question):
    fuzzy_result = matcher.find_department(question)

    if fuzzy_result:
        contact_info = f"\nNote: The official contact for this department is {fuzzy_result}."
    else:
        contact_info = ""

    context = retrieve_context(question)
    combined_context = context + contact_info
    answer = query_deepseek(question, combined_context)
    return answer
'''


# =========================================================
# KEEP THIS EXACT STYLE FROM YOUR ORIGINAL STARTER
# =========================================================
def mock_ask(question):
    question = (question or "").strip()

    if not question:
        return "Please enter a question."

    q = question.lower()

    if "lesson" in q or "today" in q or "timetable" in q:
        return (
            "Today is Thursday:\n"
            "9:00 – 11:00 (Cyber Security)\n"
            "12:00 – 14:00 (Digital Forensics)"
        )

    if "room" in q or "rooms" in q:
        return (
            "For Cyber Security you are in room HW1/14\n"
            "For Digital Forensics you are in room OA1/04"
        )

    if "it" in q or "support" in q:
        return "You can contact IT Support at: itsupport@university.ac.uk"

    if "course" in q:
        return "Course information is available through the student portal, module handbook, or your course leader."

    if "faq" in q:
        return "You can ask about timetables, rooms, deadlines, accessibility, IT support, and general university FAQs."

    return f"UI TEST: You asked '{question}'. The AI reply appears here."


# =========================================================
# SINGLE PLACE TO SWITCH FROM MOCK TO REAL AI LATER
# =========================================================
def bot_response(question):
    return mock_ask(question)
    # return ask_question(question)


# =========================================================
# UI LOGIC
# =========================================================
def login_user(username, password):
    if username.strip() and password.strip():
        return (
            gr.update(visible=False),
            gr.update(visible=True),
            "Login successful. Welcome back."
        )

    return (
        gr.update(visible=True),
        gr.update(visible=False),
        "Please enter both username and password."
    )


def send_message(user_message, history):
    if history is None:
        history = [{"role": "assistant", "content": "How may I assist you today?"}]

    user_message = (user_message or "").strip()

    if not user_message:
        return "", history

    answer = bot_response(user_message)

    history = history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": answer}
    ]

    return "", history


def quick_reply(choice, history):
    if history is None:
        history = [{"role": "assistant", "content": "How may I assist you today?"}]

    answer = bot_response(choice)

    history = history + [
        {"role": "user", "content": choice},
        {"role": "assistant", "content": answer}
    ]

    return history


def attach_placeholder(history):
    if history is None:
        history = [{"role": "assistant", "content": "How may I assist you today?"}]

    history = history + [
        {
            "role": "assistant",
            "content": "Attach button is ready for future file upload support."
        }
    ]
    return history


# =========================================================
# STYLING
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
    padding: 18px 22px;
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
    padding: 18px;
}

.ai-badge {
    width: 54px;
    height: 54px;
    min-width: 54px;
    border-radius: 50%;
    background: #0b79c7;
    color: white;
    border: 2px solid #183848;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.05rem;
    margin-top: 3px;
}

.user-badge {
    width: 54px;
    height: 54px;
    min-width: 54px;
    border-radius: 50%;
    background: #05b84d;
    color: white;
    border: 2px solid #183848;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.05rem;
    margin-top: 3px;
}

.ai-bar textarea,
.ai-bar input {
    background: #4ea8d3 !important;
    color: white !important;
    border: 2px solid #214253 !important;
    border-radius: 12px !important;
    font-size: 1.05rem !important;
}

.ai-bar textarea::placeholder,
.ai-bar input::placeholder {
    color: rgba(255,255,255,0.96) !important;
}

.green-box input,
.green-box textarea {
    background: #05b84d !important;
    color: white !important;
    border: 2px solid #214253 !important;
    border-radius: 10px !important;
    font-size: 1rem !important;
    min-height: 48px !important;
}

.green-box input::placeholder,
.green-box textarea::placeholder {
    color: rgba(255,255,255,0.96) !important;
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

.secondary-btn button {
    background: #4ea8d3 !important;
    color: white !important;
    border: 2px solid #214253 !important;
    border-radius: 12px !important;
    min-height: 50px !important;
    font-size: 1rem !important;
}

.quick-btn button {
    background: #4ea8d3 !important;
    color: white !important;
    border: 2px solid #214253 !important;
    border-radius: 12px !important;
    min-height: 58px !important;
    font-size: 1rem !important;
    text-align: left !important;
    justify-content: flex-start !important;
}

.arrow-btn button {
    background: #145f82 !important;
    color: white !important;
    border: 2px solid #214253 !important;
    border-radius: 10px !important;
    min-height: 50px !important;
    font-size: 1.2rem !important;
}

.attach-btn button {
    background: white !important;
    color: black !important;
    border: 2px solid #214253 !important;
    border-radius: 8px !important;
    min-height: 44px !important;
}

.info-tile {
    background: #145f82;
    color: white;
    border: 2px solid #0d445b;
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 1.05rem;
    text-align: center;
    font-weight: 500;
}

.chatbot-wrap {
    border: 2px solid #214253 !important;
    border-radius: 16px !important;
    background: white !important;
    overflow: hidden !important;
}

.query-box input,
.query-box textarea {
    border: 2px solid #214253 !important;
    border-radius: 0 !important;
    min-height: 44px !important;
}

.gr-box, .gr-group, .gr-panel {
    box-shadow: none !important;
}
"""


# =========================================================
# THIS REPLACES gr.Interface(...) BUT KEEPS interface = ...
# =========================================================
with gr.Blocks(
    css=custom_css,
    title="University Chatbot"
) as interface:

    gr.HTML("""
        <div class="topbar">
            <h1>MyHud</h1>
            <div class="close-btn">✕</div>
        </div>
    """)

    with gr.Column(elem_classes="main-wrap"):
        status_msg = gr.Markdown("")

        with gr.Row():
            # LEFT PANEL
            with gr.Column(scale=1):
                with gr.Group(visible=True) as login_panel:
                    with gr.Row():
                        gr.HTML('<div class="ai-badge">AI</div>')
                        gr.Textbox(
                            value="To Access all Features Please Login.",
                            interactive=False,
                            show_label=False,
                            elem_classes="ai-bar"
                        )

                    with gr.Row():
                        gr.HTML("<div></div>")
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
                                placeholder="Please Enter Username.......",
                                show_label=False,
                                elem_classes="green-box"
                            )

                    with gr.Row():
                        with gr.Column(scale=1, min_width=120):
                            gr.HTML('<div class="label-chip">Password</div>')
                        with gr.Column(scale=4):
                            password = gr.Textbox(
                                placeholder="Please Enter Password.......",
                                type="password",
                                show_label=False,
                                elem_classes="green-box"
                            )

                    with gr.Row():
                        gr.HTML("<div></div>")
                        login_btn = gr.Button("Login", elem_classes="primary-btn")

            # RIGHT PANEL
            with gr.Column(scale=1):
                with gr.Row():
                    gr.HTML('<div class="ai-badge">AI</div>')
                    gr.Textbox(
                        value="How may I assist you today?",
                        interactive=False,
                        show_label=False,
                        elem_classes="ai-bar"
                    )

                with gr.Row():
                    pre_q1 = gr.Button("Looking for Timetable information?", elem_classes="quick-btn")
                    pre_q1_arrow = gr.Button("➜", elem_classes="arrow-btn")

                with gr.Row():
                    pre_q2 = gr.Button("Course Information?", elem_classes="quick-btn")
                    pre_q2_arrow = gr.Button("➜", elem_classes="arrow-btn")

                with gr.Row():
                    pre_q3 = gr.Button("Contact IT Support", elem_classes="quick-btn")
                    pre_q3_arrow = gr.Button("➜", elem_classes="arrow-btn")

                with gr.Row():
                    pre_q4 = gr.Button("Click Here For Frequently Asked Questions", elem_classes="quick-btn")
                    pre_q4_arrow = gr.Button("➜", elem_classes="arrow-btn")

        with gr.Group(visible=False) as dashboard_panel:
            with gr.Row():
                gr.HTML('<div class="ai-badge">AI</div>')
                gr.Textbox(
                    value="How may I assist you today?",
                    interactive=False,
                    show_label=False,
                    elem_classes="ai-bar"
                )

            chatbot = gr.Chatbot(
                value=[{"role": "assistant", "content": "How may I assist you today?"}],
                type="messages",
                height=330,
                elem_classes="chatbot-wrap"
            )

            with gr.Row():
                dash_q1 = gr.Button("What lessons do I have today?", elem_classes="secondary-btn")
                dash_q2 = gr.Button("Which rooms are my lessons in?", elem_classes="secondary-btn")
                dash_q3 = gr.Button("See Full Timetable", elem_classes="secondary-btn")
                dash_q3_arrow = gr.Button("➜", elem_classes="arrow-btn")

            with gr.Row():
                gr.HTML('<div class="info-tile">Next Lesson: 1hr 30 mins</div>')
                gr.HTML('<div class="info-tile">Assignment Due: 05/03/26</div>')

        with gr.Row():
            query_box = gr.Textbox(
                placeholder="Please Enter A Query.....",
                show_label=False,
                scale=8,
                elem_classes="query-box"
            )
            attach_btn = gr.Button("Attach", elem_classes="attach-btn", scale=1)
            send_btn = gr.Button("➜", elem_classes="arrow-btn", scale=1)

    # EVENTS
    login_btn.click(
        fn=login_user,
        inputs=[username, password],
        outputs=[login_panel, dashboard_panel, status_msg]
    )

    send_btn.click(
        fn=send_message,
        inputs=[query_box, chatbot],
        outputs=[query_box, chatbot]
    )

    query_box.submit(
        fn=send_message,
        inputs=[query_box, chatbot],
        outputs=[query_box, chatbot]
    )

    attach_btn.click(
        fn=attach_placeholder,
        inputs=[chatbot],
        outputs=[chatbot]
    )

    pre_q1.click(
        fn=lambda history: quick_reply("Looking for timetable information?", history),
        inputs=[chatbot],
        outputs=[chatbot]
    )
    pre_q1_arrow.click(
        fn=lambda history: quick_reply("Looking for timetable information?", history),
        inputs=[chatbot],
        outputs=[chatbot]
    )

    pre_q2.click(
        fn=lambda history: quick_reply("Course Information?", history),
        inputs=[chatbot],
        outputs=[chatbot]
    )
    pre_q2_arrow.click(
        fn=lambda history: quick_reply("Course Information?", history),
        inputs=[chatbot],
        outputs=[chatbot]
    )

    pre_q3.click(
        fn=lambda history: quick_reply("Contact IT Support", history),
        inputs=[chatbot],
        outputs=[chatbot]
    )
    pre_q3_arrow.click(
        fn=lambda history: quick_reply("Contact IT Support", history),
        inputs=[chatbot],
        outputs=[chatbot]
    )

    pre_q4.click(
        fn=lambda history: quick_reply("FAQ", history),
        inputs=[chatbot],
        outputs=[chatbot]
    )
    pre_q4_arrow.click(
        fn=lambda history: quick_reply("FAQ", history),
        inputs=[chatbot],
        outputs=[chatbot]
    )

    dash_q1.click(
        fn=lambda history: quick_reply("What lessons do I have today?", history),
        inputs=[chatbot],
        outputs=[chatbot]
    )

    dash_q2.click(
        fn=lambda history: quick_reply("Which rooms are my lessons in?", history),
        inputs=[chatbot],
        outputs=[chatbot]
    )

    dash_q3.click(
        fn=lambda history: quick_reply("Show me my full timetable", history),
        inputs=[chatbot],
        outputs=[chatbot]
    )
    dash_q3_arrow.click(
        fn=lambda history: quick_reply("Show me my full timetable", history),
        inputs=[chatbot],
        outputs=[chatbot]
    )

interface.launch()