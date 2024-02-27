import logging
logging.basicConfig(level=logging.ERROR)
logging.error('This will get logged')
import os
import fitz
from dotenv import load_dotenv
load_dotenv()

if os.getenv("OPENAI_API_KEY") is not None:
    print("OPENAI_API_KEY is ready")
else:
    print("OPENAI_API_KEY is failing")

from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles

from qdrant_client import QdrantClient
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

embeddings = OpenAIEmbeddings()
collection_name = "resume_test"
client = QdrantClient("localhost", port=6333)
qdrant = Qdrant(client, collection_name, embeddings)

url = "localhost:6333"
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

pages = ()

# @app.get("/processPDF")
# def main():
#     print("Starting the process...")
#     pdf_data = ()
   
#     #Step 1: load PDF into array of documents
#     try:
#         pdf_data = load_pdf()
#         print("pdf loaded")
#     except:
#         print("error step 1: load pdf")
    
#     #Step 2: load data into qdrant 
#     try:
#         load_qdrant(pdf_data)
#         print("data loaded into qdrant")
#     except Exception as e:
#         logging.error("Exception occurred", exc_info=True)
#         print("error step 2: load data into qdrant")

@app.get("/query_resume")
async def query_qdrant(question: str = Query(..., description="A question about Ernest's resume")):
    
    pdf_data = []
   
    #Step 1: load PDF into array of documents
    try:
        pdf_data = load_pdf()
        # pdf_data = minimal_load_pdf()
        print("pdf loaded", pdf_data)
    except:
        print("error step 1: load pdf")
    
    #Step 2: load data into qdrant 
    try:
        print("data to be loaded into qdrant:", pdf_data)
        load_qdrant(pdf_data)
        print("data loaded into qdrant")
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        print("error step 2: load data into qdrant")

    #Step 3. ask question
    try:
        response_answer = get_answer(question, pdf_data)
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        print("error step 3: ask question")

def load_pdf():
    # Open the PDF file
    loader = PyPDFLoader("/Users/jason/repos/se-challenge-codeslip/PDFs/Ernest_Hemingway_Resume.pdf")
    pages = loader.load_and_split()
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = text_splitter.split_documents(pages)
    for doc in docs:
            # Assuming 'doc' is a dictionary and 'page_content' is a key
            # Convert 'page_content' to string if it's not already
            if 'page_content' in doc and not isinstance(doc['page_content'], str):
                print("page_content in the correct location")
                doc['page_content'] = str(doc['page_content'])
    return docs

def load_qdrant(pdf_data):
    qdrant_load = qdrant.from_documents(
        pdf_data,
        embeddings,
        url=url,
        collection_name= collection_name,
        content_payload_key= collection_name,
        metadata_payload_key= collection_name
    )
    print("qdrant loaded: ", qdrant_load)

def get_answer(question, pdf_data):
    qdrant_get = qdrant.from_documents(
        pdf_data,
        embeddings,
        url=url,
        collection_name= collection_name,
        content_payload_key= collection_name,
        metadata_payload_key= collection_name
    )

    print("Question:", question)
    answer = qdrant_get.similarity_search(question)
    print(answer[0].page_content)
  
    # return answer 

    # # Convert text query into vector
    # vector = qdrant.encode(question).tolist()

    # # Use `vector` for search for closest vectors in the collection
    # search_result = qdrant.qdrant_client.search(
    #     collection_name= collection_name,
    #     query_vector=vector,
    #     query_filter=None,  # If you don't want any filters for now
    #     limit=5,  # 5 the most closest results is enough
    # )
    
    # payloads = [hit.payload for hit in search_result]
    # print("payloads:",payloads)
    # return payloads
    