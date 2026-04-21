import re
import gradio as gr
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM, OllamaEmbeddings
import os
from VectorStore import VectorStore
from Fuzzymatching import Fuzzymatch

class Chatbot:
    def __init__(self, persist_path, pdf_path, excel_path, llm_model, embed_model="nomic-embed-text"):
        self.persist_path = persist_path
        self.pdf_path = pdf_path
        self.matcher = Fuzzymatch(excel_path)
        self.llm = OllamaLLM(model=llm_model)

<<<<<<< HEAD
        
=======
        # VectorStore management
>>>>>>> UI_QAMAR
        self.kb_manager = VectorStore(
            persist_path=self.persist_path, 
            path_to_pdf=self.pdf_path, 
            embed_model=embed_model
        )
        
        self.vector_db = self.kb_manager.returnDB()
        self.retriever = self.vector_db.as_retriever()

    def query_deepseek(self, question, context):
<<<<<<< HEAD
      
        
        
        
        
        
=======
>>>>>>> UI_QAMAR
        system_instruction = (
            "### ROLE ###\n"
            "You are the University of Huddersfield Official Assistant.\n\n"
            "### RULES ###\n"
            "1. ONLY use the provided 'Context' below. Do NOT use your own knowledge.\n"
            "2. If the answer is not in the Context, say: 'I am sorry, I don't have that information. Please contact the student hub at study@hud.ac.uk.'\n"
            "3. Do NOT mention other universities or generic external links.\n"
            "4. If the user's input is a greeting (e.g., 'Hello', 'Hi', 'Hey', 'Good morning'), ignore the Context for a moment and respond ONLY with: 'I am the university chatbot, how can I help you today?'"
        )

        prompt = (
            f"{system_instruction}\n"
            f"### CONTEXT ###\n{context}\n\n"
            f"### QUESTION ###\n{question}\n"
            "### FINAL ANSWER ###"
        )
        
<<<<<<< HEAD
        
=======
>>>>>>> UI_QAMAR
        response = self.llm.invoke(prompt)
        final_answer = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
        return final_answer

    def retrieve_context(self, question):
        results = self.retriever.invoke(question)
        print(f"DEBUG: Found {len(results)} chunks for search.")
        context = "\n\n".join([doc.page_content for doc in results])
        return context

    def ask_question(self, question):
        fuzzy_result = self.matcher.find_department(question)
        contact_info = f"\nNote: The official contact for this department is {fuzzy_result}." if fuzzy_result else ""
        
<<<<<<< HEAD
        
        # If a match was found, add it to our knowledge
        if fuzzy_result:
            contact_info = f"\nNote: The official contact for this department is {fuzzy_result}."
        else:
            contact_info = ""

        #  Get general context from Vector DB 
=======
>>>>>>> UI_QAMAR
        context = self.retrieve_context(question)
        combined_context = context + contact_info
        
<<<<<<< HEAD
        #  Send everything to DeepSeek 
=======
>>>>>>> UI_QAMAR
        answer = self.query_deepseek(question, combined_context)
        return answer

    def _render_chat(self, history):
        """Helper to turn history list into the custom HTML bubbles"""
        html = '<div class="chat-area">'
        for msg in history:
            if msg["role"] == "ai":
                html += f'''
                <div class="msg-row">
                    <div class="circle ai-circle">AI</div>
                    <div class="bubble ai-bubble">{msg["content"]}</div>
                </div>'''
            else:
                html += f'''
                <div class="msg-row user-row">
                    <div class="bubble user-bubble">{msg["content"]}</div>
                    <div class="circle user-circle">You</div>
                </div>'''
        html += '</div>'
        return html

    def launch_ui(self):
        custom_css = """
        /* 1. Import a premium modern font from Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

     
        body, .gradio-container { 
            background: #e7e7e7 !important; 
            font-family: 'Outfit', -apple-system, sans-serif !important; 
            -webkit-font-smoothing: antialiased;
            text-rendering: optimizeLegibility;
        }

      
        .gradio-container { 
            max-width: 1100px !important; 
            width: 95% !important;
            margin: 20px auto !important; 
            padding: 0 !important; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1); /* Adds depth */
        }

        footer { display: none !important; }

       
        .topbar { 
            background: #145f82; 
            color: white; 
            padding: 20px; 
            border: 2px solid #0d445b; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        .topbar h1 { 
            margin: 0; 
            font-size: 1.8rem; 
            font-weight: 600; 
            letter-spacing: -0.02em; 
        }

      
        .close-btn { display: none !important; }

    
        .main-wrap { 
            width: 100% !important;
            padding: 25px 20px; 
            min-height: 550px; 
            max-height: 70vh; 
            box-sizing: border-box; 
            border-left: 2px solid #145f82; 
            border-right: 2px solid #145f82; 
            overflow-y: auto; 
            background: #ffffff;
            display: flex !important;
            flex-direction: column !important;
        }

        .chat-area {
            width: 100% !important;
        }

     
        .msg-row { display: flex; align-items: flex-start; gap: 15px; margin-bottom: 20px; }
        .user-row { justify-content: flex-end; }

        .circle { 
            width: 48px; 
            height: 48px; 
            min-width: 48px; 
            border-radius: 50%; 
            border: 2px solid #183848; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            color: white; 
            font-size: 0.9rem; 
            font-weight: 600;
        }
        .ai-circle { background: #0b79c7; }
        .user-circle { background: #00B050; }

        .bubble { 
            border-radius: 18px; 
            padding: 14px 20px; 
            color: white; 
            font-size: 1.05rem; 
            line-height: 1.6; /* Balanced spacing for readability */
            max-width: 80%;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .ai-bubble { background: #4ea8d3; border-bottom-left-radius: 4px; }
        .user-bubble { background: #00B050; border-bottom-right-radius: 4px; }

        /* 8. Bottom Input Bar */
        .bottom-bar { 
            border: 2px solid #145f82; 
            padding: 10px; 
            background: white;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
        }

        .query-box textarea, .query-box input {
            border: none !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 1.05rem !important;
            padding: 10px !important;
        }

        .send-btn button {
            background: transparent !important;
            color: #145f82 !important;
            font-size: 1.6rem !important;
            transition: transform 0.2s ease;
        }
        .send-btn button:hover { transform: scale(1.1); }
        """

        with gr.Blocks(css=custom_css) as demo:
            history = gr.State([{"role": "ai", "content": "How may I assist you today?"}])

            gr.HTML("""
                <div class="topbar">
                    <h1>MyHud AI Chatbot</h1>
                    <div class="close-btn">✕</div>
                </div>
            """)

            with gr.Column(elem_classes="main-wrap"):
                chat_display = gr.HTML(self._render_chat([{"role": "ai", "content": "How may I assist you today?"}]))

            with gr.Row(elem_classes="bottom-bar"):
                txt = gr.Textbox(
                    placeholder="Please Enter A Query....",
                    show_label=False,
                    scale=9,
                    container=False
                )
                btn = gr.Button("➜", scale=1)

            def respond(user_input, current_history):
                bot_answer = self.ask_question(user_input)
                current_history.append({"role": "user", "content": user_input})
                current_history.append({"role": "ai", "content": bot_answer})
                html_output = self._render_chat(current_history)
                return html_output, current_history, ""

            btn.click(respond, [txt, history], [chat_display, history, txt])
            txt.submit(respond, [txt, history], [chat_display, history, txt])

        demo.launch()

if __name__ == "__main__":
    p_path = "/Users/Jonny/Desktop/University-chatbot/PDF faqs/University_Knowledge_Base"
    pdf_folder = "/Users/Jonny/Desktop/University-chatbot/PDF faqs" 
    e_path = "/Users/Jonny/Desktop/University-chatbot/Contact emails/CONTACT EMAILS.xlsx"

    my_bot = Chatbot(
        persist_path=p_path, 
        pdf_path=pdf_folder, 
        excel_path=e_path, 
        llm_model="deepseek-r1:1.5b"
    )
    my_bot.launch_ui()