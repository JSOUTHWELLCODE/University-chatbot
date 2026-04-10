
import re
import gradio as gr
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM , OllamaEmbeddings
import os
from VectorStore import VectorStore

from Fuzzymatching import Fuzzymatch






class Chatbot:
    def __init__(self, persist_path, pdf_path, excel_path, llm_model, embed_model="nomic-embed-text"):
        self.persist_path = persist_path
        self.pdf_path = pdf_path # Save it to the class
        self.matcher = Fuzzymatch(excel_path)
        self.llm = OllamaLLM(model=llm_model)

        
        self.kb_manager = VectorStore(
            persist_path=self.persist_path, 
            path_to_pdf=self.pdf_path, 
            embed_model=embed_model
        )
        
        self.vector_db = self.kb_manager.returnDB()
        self.retriever = self.vector_db.as_retriever()


       

    def query_deepseek(self, question, context):
      
        
        
        
        
        
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

        
        
        response = self.llm.invoke(prompt)
        
        # LangChain returns a string directly
        final_answer = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
        return final_answer

    def retrieve_context(self, question):
        # Retrieve relevant documents
        results = self.retriever.invoke(question)

        print(f"DEBUG: Found {len(results)} chunks for search.")
        # Combine the retrieved content
        context = "\n\n".join([doc.page_content for doc in results])
        return context

    def ask_question(self, question):
        # Retrieve context and generate an answer using RAG
        fuzzy_result = self.matcher.find_department(question)

        
        
        # If a match was found, add it to our knowledge
        if fuzzy_result:
            contact_info = f"\nNote: The official contact for this department is {fuzzy_result}."
        else:
            contact_info = ""

        #  Get general context from Vector DB 
        context = self.retrieve_context(question)
        
        # Combine the Excel data + the Vector DB data
        combined_context = context + contact_info
        
        #  Send everything to DeepSeek 
        answer = self.query_deepseek(question, combined_context)
        return answer

    def launch_ui(self):
        # Set up the Gradio interface
        interface = gr.Interface(
            fn=self.ask_question,
            inputs="text",
            outputs="text",
            title="University Chatbot",
            description="Answers FAQS for university website Powered by DeepSeek-R1."
        )
        interface.launch()




if __name__ == "__main__":
     # Define your paths
     p_path = "/Users/Jonny/Desktop/University-chatbot/PDF faqs/University_Knowledge_Base"
     pdf_folder = "/Users/Jonny/Desktop/University-chatbot/PDF faqs" 
     e_path = "/Users/Jonny/Desktop/University-chatbot/Contact emails/CONTACT EMAILS.xlsx"

     my_bot = chatbot(
         persist_path=p_path, 
         pdf_path=pdf_folder, 
         excel_path=e_path, 
         llm_model="deepseek-r1:1.5b"
     )
     my_bot.launch_ui()


# To run the bot:
# my_bot = chatbot(persist_path="your_path", excel_path="your_excel", llm_model="deepseek-r1:8b")
# my_bot.launch_ui()

