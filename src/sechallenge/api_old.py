import logging
import fitz #
import os
from dotenv import load_dotenv
load_dotenv()

if os.getenv("OPENAI_API_KEY") is not None:
    print("OPENAI_API_KEY is ready")
else:
    print("OPENAI_API_KEY is failing")

from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from langchain_community.vectorstores import Qdrant
#from langchain.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
#from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.VectorDBQA import VectorDBQA
#from langchain import VectorDBQA, OpenAI
from langchain_community.llms.OpenAI import OpenAI

from langchain.prompts import PromptTemplate

embedding = OpenAIEmbeddings()

llm = OpenAI()

model = SentenceTransformer("all-MiniLM-L6-v2")
logger = logging.getLogger(__name__)
client = QdrantClient("localhost", port=6333)
collection_name = "resumes_test"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def welcome():
    welcome = "Welcome to PDF analyzer"
    return welcome.strip('"')

@app.get("/hello")
def hello(name: Annotated[str, Query()] = "Wilson"):
    return {"message": f"Hello {name}!"}

@app.get("/processPDF")
def main():
    print("Starting the process...")
    pages_data = ()
    documents = []
    vectorEmbeddings = []
    qdrant_ref = ()
   
    #attempt to split the pages and extract the data
    try:
        pages_data = split_text_by_pages()
        print("split_text_by_pages completed")
    except:
        print("split_text_by_pages error")
    
    #attempt to organize data 
    try:
        documents = organize_data_into_documents(pages_data)
        print("organized documents data")
    except:
        print("organize_data_into_documents error")

    # #attempt to chunk the data
    # try:
    #     documents = organize_data_into_chunks(documents)
    #     print("organized data into chunks")
    # except:
    #     print("organize_data_into_chunks error")
    
    #attempt to generate vector embeddings from text
    try:
        vectorEmbeddings = create_vector_embeddings(documents)
        print("documents transformed into vector embeddings")
    except: 
        print("transforming documents into vector embedding failed")
    
    #attempt to initialize qdrant collection #attempt to initialize qdrant collection
    try:
        initialize_response = client.recreate_collection(
            #  switch from client.recreate to client.create_collection in production
                collection_name= collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.DOT),
            )
        if initialize_response != "True":
            #continue
            print("Collection already initialized, continue...")
        else: 
            print("New collection initialized")
    except:
        print("error intializing qdrant collection")

    try:
        qdrant_ref = store_data_in_qdrant(vectorEmbeddings, documents)
        print("store_data_in_qdrant completed")
        print("qdrant:", qdrant_ref)
    except:
        print("store_data_in_qdrant error")

def split_text_by_pages():
    # Open the PDF file
    doc = fitz.open("/Users/jason/repos/se-challenge-codeslip/PDFs/Ernest_Hemingway_Resume.pdf")
    #Initialize arrays to store data from each page
    pages_text = []  
    pages_number = [] 
    pages_title = [] 
    # Iterate over each page in the document
    for page_number, page in enumerate(doc, start=1):
        # Extract text from the current page
        text = page.get_text()
        # Extract the page title
        lines = text.split("\n")  # Split the text into lines
        title = "Ernest Hemingway Resume"
        page_title = ()
        for i, line in enumerate(lines):
            if title in line:
                # Ensure there is a next line to return
                if i + 1 < len(lines):
                    page_title = lines[i + 1]
                else:
                    page_title = ""  # Return an empty string if the title is the last line
        pages_text.append(lines)
        pages_number.append(page_number)
        pages_title.append(page_title)
    # Close the document
    doc.close()

    return pages_text, pages_number, pages_title

def organize_data_into_documents(pages_data):
    pages_text, pages_numbers, pages_titles = pages_data
    
    documents = []  # Initialize the list to store the document dictionaries

    # Iterate through the raw pages and their corresponding titles and numbers
    for index, content in enumerate(pages_text):
        page_number = str(pages_numbers[index])  # Convert page number to string
        page_title = pages_titles[index]
        
        # Join the text content, excluding the first item (which is a repeated title)
        page_text = " ".join(content[1:])  # Join the text parts into a single string
        
        # Create a dictionary for the current page and append it to the documents list
        documents.append({
            "page_number": page_number,
            "page_title": page_title,
            "page_text": page_text
        })
    
    return documents

# def organize_data_into_chunks(documents):
#     print("Create chunks")
#     for document in documents:
#         l= document["page_text"].split('.')
#         res= {}
#         for i in range(len(l)//20+1):
#             res[i]=l[i:i+20]
#         print("chunked: ",res)

def create_vector_embeddings(documents):
    print("starting embedding:", documents)
    vectors = []
    vectors = model.encode(
        [document["page_title"] + ". " + document["page_text"] for document in documents]
    )
    print("vectors:", vectors)
    return vectors

def store_data_in_qdrant(vectorEmbeddings, documents): 
    #beginning storing process
    uploadStatus = client.upload_collection(
        collection_name= collection_name,
        vectors=vectorEmbeddings,
        payload=documents,
        ids=None,  # Vector ids will be assigned automatically
        batch_size=512,  # How many vectors will be uploaded in a single request?
    )
    return uploadStatus

@app.get("/question-answer")
async def query_qdrant(question: str = Query(..., description="The natural language question")):
    
    #define the custom prompt
    custom_prompt_template = PromptTemplate(
        template= question, input_variables=["context", "question"]
    )

    answers = "test answers"
    #define the doc_store
    doc_store = Qdrant.from_texts(
        answers, embedding, host="localhost" 
    )


    qa = VectorDBQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        vectorstore=doc_store,
        return_source_documents=False,
        chain_type_kwargs={"prompt": custom_prompt_template}
    )

    print("test 2!", qa)
    
    return {"question": question, "answer": qa}