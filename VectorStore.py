
import os
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM, OllamaEmbeddings
import shutil


#path = r"Z:\Group project\PDF faqs"





class VectorStore:
    def __init__(self, persist_path , path_to_pdf, embed_model="nomic-embed-text"):
        self.persist_path = persist_path
        self.embedding_function = OllamaEmbeddings(model=embed_model)
        self.loader = DirectoryLoader(path_to_pdf, glob="**/*.pdf",  loader_cls=PyMuPDFLoader)



    def returnDB(self):
        #  Check if the folder exists AND has files in it
        sqlite_db_path = os.path.join(self.persist_path, "chroma.sqlite3")
        
        if os.path.exists(sqlite_db_path):
            print("Found existing database at path. Loading from disk...")
            
            # Load the existing database
            vectorstore = Chroma(
                persist_directory=self.persist_path,
                embedding_function=self.embedding_function,
                collection_name="faq_pdf"
            )
            return vectorstore # Return the loaded DB
        


        else: 
            print("🆕 No database found. Creating a new one...")

            # Use self.loader that you defined in __init__
            documents = self.loader.load()

            # Split the document into smaller chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

            chunks = text_splitter.split_documents(documents)
            
            # Create the DB and save it to the path
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embedding_function,
                persist_directory=self.persist_path,
                collection_name="faq_pdf"
            )
            print(f" Database created and saved to {self.persist_path}")
            return vectorstore
    

    def add_new_pdf(self, pdf_path, vectorstore):
        #  Load the single new PDF using the path provided
        loader = PyMuPDFLoader(pdf_path)
        new_docs = loader.load()

        #  Split it into chunks (using the same settings as your init)
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        new_chunks = text_splitter.split_documents(new_docs)

        #  Add to the existing Chroma object 
        vectorstore.add_documents(new_chunks)
        
        print(f" Successfully added {len(new_chunks)} chunks from {pdf_path}")


  

    def delete_database(self):
   
    
     if os.path.exists(persist_path):
        shutil.rmtree(persist_path)
        return f"Database at '{persist_path}' deleted successfully."
     else:
        return f"folder '{persist_path}' not found. Nothing to delete."






if __name__ == "__main__":
    '''
    # 1. Initialize/Load the Database
    vector_db = returnDB(embedding_function, persist_path)

    # 2. Create the Retriever 
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    #Add new chunks to the Data base 
    #add_new_pdf_to_db("/Users/Jonny/Desktop/University-chatbot/PDF faqs/IT_SUPPORT.pdf", vector_db)

    '''

    persist_path = r"/Users/Jonny/Desktop/University-chatbot/PDF faqs/University_Knowledge_Base"
    path_to_PDF = r"/Users/Jonny/Desktop/University-chatbot/PDF faqs"

    kb_manager = VectorStore(persist_path, embed_model="nomic-embed-text", path_to_pdf=path_to_PDF)


    vector_db = kb_manager.returnDB()

 
    if vector_db:
        retriever = vector_db.as_retriever(search_kwargs={"k": 3})
        print("✅ Retriever is ready for testing!")


    






        

















