
import os
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM, OllamaEmbeddings


#path = r"Z:\Group project\PDF faqs"


#_________MAC PAth
persist_path = r"/Users/Jonny/Desktop/University-chatbot/PDF faqs/University_Knowledge_Base"



#path to FAQ folders 
#loader = DirectoryLoader(r"Z:\Group project\PDF faqs", glob="**/*.pdf",  loader_cls=PyMuPDFLoader)


#_____MAC
loader = DirectoryLoader(r"/Users/Jonny/Desktop/University-chatbot/PDF faqs"
, glob="**/*.pdf",  loader_cls=PyMuPDFLoader)





# Initialize Ollama embeddings using DeepSeek-R1
embedding_function = OllamaEmbeddings(model="nomic-embed-text")




persist_path = "/Users/Jonny/Desktop/University-chatbot/PDF faqs/University_Knowledge_Base"




def returnDB(embedding_function, persist_path):
    # 1. Check if the folder exists AND has files in it

    sqlite_db_path = os.path.join(persist_path, "chroma.sqlite3")
    if os.path.exists(sqlite_db_path):
        print("Found existing database at path. Loading from disk...")
        
        # Load the existing database
        vectorstore = Chroma(
            persist_directory=persist_path,
            embedding_function=embedding_function,
            collection_name="faq_pdf"
        )
        return vectorstore # Return the loaded DB
       
    else: 
        print("🆕 No database found. Creating a new one...")



        documents = loader.load()

        # Split the document into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        chunks = text_splitter.split_documents(documents)
        


        # Create the DB and save it to the path
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_function,
            persist_directory=persist_path,
            collection_name="faq_pdf"
        )
        print(f" Database created and saved to {persist_path}")
        return vectorstore




def add_new_pdf_to_db(pdf_path, vectorstore):
    # 1. Load the single new PDF
    loader = PyMuPDFLoader(pdf_path)
    new_docs = loader.load()

    # 2. Split it into chunks (use the same settings as before!)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    new_chunks = text_splitter.split_documents(new_docs)

    # 3. Add to existing Chroma object
    vectorstore.add_documents(new_chunks)
    
    print(f"✅ Successfully added {len(new_chunks)} chunks from {pdf_path}")
       





if __name__ == "__main__":
    # 1. Initialize/Load the Database
    vector_db = returnDB(embedding_function, persist_path)

    # 2. Create the Retriever 
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    #Add new chunks to the Data base 
    #add_new_pdf_to_db("/Users/Jonny/Desktop/University-chatbot/PDF faqs/IT_SUPPORT.pdf", vector_db)

    














