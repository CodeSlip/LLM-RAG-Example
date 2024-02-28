import logging
logging.basicConfig(level=logging.ERROR)
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

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings

from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA


llm = OpenAI()

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = OpenAIEmbeddings()
collection_name = "resume_test"
client = QdrantClient("localhost", port=6333)
qdrant = Qdrant(client, 
                collection_name, 
                embeddings)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/query_resume")
async def query_qdrant(question: str = Query(..., description="A question about Ernest's resume")):
    docs = ()
    answer = ()
   
    #Step 1: load PDF into array of documents
    try:
        docs = load_pdf()
        # pdf_data = minimal_load_pdf()
    except:
        print("error step 1: load pdf")
    
    #Step 2: answer question
    try:
        answer = answer_question(docs, question)
        print("data loaded into qdrant")
        print("---", answer)
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        print("error step 2: load data into qdrant")

    return answer

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

def answer_question(docs, question):

    # Define qdrant
    vectorstore = qdrant.from_documents(
        documents= docs,
        embedding= embeddings
    )

    # Define retriever
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs = {"k":2}
    )

    # Define prompt structure
    prompt = f"""
    <|system|>
    You are an AI assistant that receives questions about resumes, and responds with answers from your knowledge base.
    </s>
    <|user|>
    {question}
    </s>
    <|assistant|>
    """

    # Get response from llm
    response = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    answer = response.invoke(prompt)["result"]

    return answer
