import ollama
import re
import gradio as gr
#from concurrent.futures import ThreadPoolExecutor

custom_css = """
.topbar {
    background-color: #f0f0f0;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.main-wrap {
    max-width: 1200px;
    margin: 0 auto;
}
.ai-badge {
    background-color: #007bff;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    font-weight: bold;
}
.ai-bar {
    background-color: #e3f2fd;
    border: 1px solid #007bff;
}
.primary-btn {
    background-color: #28a745;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
.secondary-btn {
    background-color: #6c757d;
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
.quick-btn {
    background-color: #17a2b8;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
.arrow-btn {
    background-color: transparent;
    border: none;
    cursor: pointer;
    font-size: 18px;
}
.green-box {
    border: 2px solid #28a745;
    border-radius: 5px;
    padding: 8px;
}
.label-chip {
    background-color: #e9ecef;
    padding: 5px 10px;
    border-radius: 5px;
    font-weight: bold;
}
.chat-panel {
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 5px;
    background-color: #f9f9f9;
    max-height: 400px;
    overflow-y: auto;
}
.message-ai {
    background-color: #e3f2fd;
    padding: 10px;
    border-radius: 5px;
    margin: 5px 0;
}
.message-user {
    background-color: #c8e6c9;
    padding: 10px;
    border-radius: 5px;
    margin: 5px 0;
}
.user-badge {
    background-color: #4caf50;
    color: white;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-weight: bold;
}
.info-tile {
    background-color: #fff3cd;
    padding: 10px;
    border-radius: 5px;
    margin: 5px;
    flex: 1;
}
.query-box {
    border: 2px solid #007bff;
    border-radius: 5px;
    padding: 10px;
}
.attach-btn {
    background-color: #6c757d;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
.close-btn {
    cursor: pointer;
    font-size: 24px;
    font-weight: bold;
}
"""

'''

from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.config import Settings
from chromadb import Client, chromadb
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM , OllamaEmbeddings
import os
from VectorStore import returnDB

from Fuzzymatching import Fuzzymatch



'''


'''

matcher = Fuzzymatch("/Users/Jonny/Desktop/University-chatbot/Contact emails/CONTACT EMAILS.xlsx")

# Load the document using PyMuPDFLoader
#loader = PyMuPDFLoader("/Users/Jonny/Desktop/University-chatbot/PDF faqs/FAQS clearing.pdf")


path = "/Users/Jonny/Desktop/University-chatbot/PDF faqs/FAQS clearing.pdf"


persist_path = "/Users/Jonny/Desktop/University-chatbot/PDF faqs/University_Knowledge_Base"



# Initialize Ollama embeddings using DeepSeek-R1
embedding_function = OllamaEmbeddings(model="deepseek-r1:1.5b")


llm = OllamaLLM(model="deepseek-r1:1.5b")




# 1. Get the Database Object 
vector_db = returnDB(embedding_function, persist_path)




retriever = vector_db.as_retriever()



def query_deepseek(question, context):
    # 1. Format the input prompt into a single string
    prompt = (
        "You are a University Assistant at the university of Huddersfield. Use the provided Context to answer the Question. "
        "If the Question is just a greeting (like 'Hello' or 'Hi'), just say 'Hello! How can I help you with the information about the university?' "
        "Otherwise, use the context provided below.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}"
    )
    
    # 2. Use LangChain's .invoke() on the llm object
    # Notice we just pass the prompt string directly!
    response = llm.invoke(prompt)
    
    # 3. Clean and return the response
    # LangChain returns a string directly, so we don't need response['message']
    final_answer = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
    return final_answer

def retrieve_context(question):
    # Retrieve relevant documents
    results = retriever.invoke(question)
    # Combine the retrieved content
    context = "\n\n".join([doc.page_content for doc in results])
    return context


def ask_question(question):
    # Retrieve context and generate an answer using RAG
    
    fuzzy_result = matcher.find_department(question)
    
    # If a match was found, we add it to our knowledge
    if fuzzy_result:
        contact_info = f"\nNote: The official contact for this department is {fuzzy_result}."
    else:
        contact_info = ""

    # --- 3. Step Two: Get general context from Vector DB ---
    context = retrieve_context(question)
    
    # Combine the Excel data + the Vector DB data
    combined_context = context + contact_info
    
    # --- 4. Step Three: Send everything to DeepSeek ---
    answer = query_deepseek(question, combined_context)
    return answer

'''


def mock_ask(question):
    return f"UI TEST: You asked '{question}'. The ai reply here."





# Set up the Gradio interface
interface = gr.Interface(
    fn=mock_ask,
    inputs="text",
    outputs="text",
    title="University Chatbot",
    description="Anwsers FAQS for university website Powered by DeepSeek-R1."
)
interface.launch()
import gradio as gr

# =========================================================
# LAYOUT-ONLY CSS
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

.chat-panel {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.message-ai {
    background: #4ea8d3;
    color: white;
    border: 2px solid #214253;
    border-radius: 12px;
    padding: 14px 16px;
    font-size: 1rem;
    width: 100%;
    box-sizing: border-box;
}

.message-user {
    background: #05b84d;
    color: white;
    border: 2px solid #214253;
    border-radius: 12px;
    padding: 14px 16px;
    font-size: 1rem;
    width: 100%;
    box-sizing: border-box;
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
# LAYOUT ONLY
# =========================================================
with gr.Blocks() as interface:
    gr.HTML("""
        <div class="topbar">
            <h1>MyHud</h1>
            <div class="close-btn">✕</div>
        </div>
    """)

    with gr.Column(elem_classes="main-wrap"):

        # -----------------------------------------
        # TOP AREA - LOGIN MOCKUP + QUICK OPTIONS
        # -----------------------------------------
        with gr.Row():
            # LEFT SIDE
            with gr.Column(scale=1):
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
                        gr.Textbox(
                            placeholder="Please Enter Username.......",
                            show_label=False,
                            elem_classes="green-box"
                        )

                with gr.Row():
                    with gr.Column(scale=1, min_width=120):
                        gr.HTML('<div class="label-chip">Password</div>')
                    with gr.Column(scale=4):
                        gr.Textbox(
                            placeholder="Please Enter Password.......",
                            type="password",
                            show_label=False,
                            elem_classes="green-box"
                        )

                with gr.Row():
                    gr.HTML("<div></div>")
                    gr.Button("Login", elem_classes="primary-btn")

            # RIGHT SIDE
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

        # -----------------------------------------
        # DASHBOARD / CHAT LAYOUT MOCKUP
        # -----------------------------------------
        gr.Markdown("### Dashboard Layout Preview")

        with gr.Column(elem_classes="chat-panel"):
            with gr.Row():
                gr.HTML('<div class="ai-badge">AI</div>')
                gr.HTML('<div class="message-ai">How may I assist you today?</div>')

            with gr.Row():
                gr.HTML('<div style="width:54px;"></div>')
                gr.HTML('<div class="message-user">What lessons do I have today?</div>')
                gr.HTML('<div class="user-badge">S</div>')

            with gr.Row():
                gr.HTML('<div class="ai-badge">AI</div>')
                gr.HTML('<div class="message-ai">Today is Thursday:<br>9:00 – 11:00 (Cyber Security)<br>12:00 – 14:00 (Digital Forensics)</div>')

            with gr.Row():
                gr.HTML('<div style="width:54px;"></div>')
                gr.Button("See Full Timetable", elem_classes="secondary-btn")
                gr.Button("➜", elem_classes="arrow-btn")

            with gr.Row():
                gr.HTML('<div class="ai-badge">AI</div>')
                gr.HTML('<div class="message-ai">What else would you like me to assist you with?</div>')

            with gr.Row():
                gr.HTML('<div class="info-tile">Next Lesson: 1hr 30 mins</div>')
                gr.HTML('<div class="info-tile">Assignment Due: 05/03/26</div>')

        # -----------------------------------------
        # BOTTOM QUERY BAR LAYOUT
        # -----------------------------------------
        with gr.Row():
            gr.Textbox(
                placeholder="Please Enter A Query.....",
                show_label=False,
                scale=8,
                elem_classes="query-box"
            )
            gr.Button("Attach", elem_classes="attach-btn", scale=1)
            gr.Button("➜", elem_classes="arrow-btn", scale=1)

interface.launch(css=custom_css)