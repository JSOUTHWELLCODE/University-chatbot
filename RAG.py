
import re
import gradio as gr
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM , OllamaEmbeddings
import os
from VectorStore import returnDB

from Fuzzymatching import Fuzzymatch








class chatbot:
    def __init__(self, persist_path, excel_path, llm_model, embed_model="nomic-embed-text"):
        self.persist_path = persist_path
        self.matcher = Fuzzymatch(excel_path)
        self.embedding_function = OllamaEmbeddings(model=embed_model)
        self.llm = OllamaLLM(model=llm_model)

        self.vector_db = returnDB(self.embedding_function, self.persist_path)
        self.retriever = self.vector_db.as_retriever()

    def query_deepseek(self, question, context):
        # 1. Format the input prompt into a single string
        prompt = (
            "You are a University Assistant at the university of Huddersfield. Use the provided Context to answer the Question. "
            "If the Question is just a greeting (like 'Hello' or 'Hi'), just say 'Hello! How can I help you with the information about the university?' "
            "Otherwise, use the context provided below.\n\n"
            f"Context: {context}\n\n"
            f"Question: {question}"
        )
        
        # 2. Use LangChain's .invoke() on the llm object
        response = self.llm.invoke(prompt)
        
        # LangChain returns a string directly
        final_answer = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
        return final_answer

    def retrieve_context(self, question):
        # Retrieve relevant documents
        results = self.retriever.invoke(question)
        # Combine the retrieved content
        context = "\n\n".join([doc.page_content for doc in results])
        return context

    def ask_question(self, question):
        # Retrieve context and generate an answer using RAG
        fuzzy_result = self.matcher.find_department(question)
        
        # If a match was found, we add it to our knowledge
        if fuzzy_result:
            contact_info = f"\nNote: The official contact for this department is {fuzzy_result}."
        else:
            contact_info = ""

        # --- 3. Step Two: Get general context from Vector DB ---
        context = self.retrieve_context(question)
        
        # Combine the Excel data + the Vector DB data
        combined_context = context + contact_info
        
        # --- 4. Step Three: Send everything to DeepSeek ---
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

     my_bot = chatbot(persist_path="/Users/Jonny/Desktop/University-chatbot/PDF faqs/University_Knowledge_Base", excel_path =r"/Users/Jonny/Desktop/University-chatbot/Contact emails/CONTACT EMAILS.xlsx", llm_model="deepseek-r1:1.5b")
     my_bot.launch_ui()



# To run the bot:
# my_bot = chatbot(persist_path="your_path", excel_path="your_excel", llm_model="deepseek-r1:8b")
# my_bot.launch_ui()

