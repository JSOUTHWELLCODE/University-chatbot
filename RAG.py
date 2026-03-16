import ollama
import re
import gradio as gr
from concurrent.futures import ThreadPoolExecutor

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
