import pytest
import os
from VectorStore import VectorStore
from RAG import Chatbot



import pytest
from RAG import Chatbot 

def test_RAG():
    
    p_path = "/Users/Jonny/Desktop/University-chatbot/PDF faqs/University_Knowledge_Base"
    pdf_folder = "/Users/Jonny/Desktop/University-chatbot/PDF faqs" 
    e_path = "/Users/Jonny/Desktop/University-chatbot/Contact emails/CONTACT EMAILS.xlsx"

   
    my_bot = Chatbot(
        persist_path=p_path, 
        pdf_path=pdf_folder, 
        excel_path=e_path, 
        llm_model="deepseek-r1:1.5b"
    )

    #  Call the main logic and save the answer
    response = my_bot.ask_question("What is UCAS?")
    
    
    assert response is not None
    assert "UCAS" in response or "sorry" in response
     







