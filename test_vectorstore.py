import pytest
import os
from VectorStore import VectorStore
from langchain_chroma import Chroma


persist_path = r"/Users/Jonny/Desktop/University-chatbot/PDF faqs/University_Knowledge_Base"
path_to_PDF = r"/Users/Jonny/Desktop/University-chatbot/PDF faqs"

def test_returndb():
    """Checks if a chroma object is created and saved correctly."""
    
   
    kb_manager = VectorStore(
        persist_path=persist_path, 
        embed_model="nomic-embed-text", 
        path_to_pdf=path_to_PDF
    )

    #  Test the Database Loading/Creation
    vector_db = kb_manager.returnDB()


    assert vector_db is not None
    assert isinstance(vector_db, Chroma)









