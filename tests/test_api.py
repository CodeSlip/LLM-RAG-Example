import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from sechallenge.api import app, load_pdf, answer_question

client = TestClient(app)

def test_hello():
    with TestClient(app) as client:
        response = client.get("/hello?name=Reba")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello Reba!"}
        assert client.get("/hello").json() == {"message": "Hello Wilson!"}

def test_load_pdf():
    # Mocking PyPDFLoader and CharacterTextSplitter behavior
    with patch('your_module.PyPDFLoader') as MockLoader:
        with patch('your_module.CharacterTextSplitter') as MockSplitter:
            MockLoader.return_value.load_and_split.return_value = ["page content"]
            MockSplitter.return_value.split_documents.return_value = [{'page_content': 'Ernest Hemingway Resume'}]
            docs = load_pdf()
            assert len(docs) == 1
            assert docs[0]['page_content'] == 'Ernest Hemingway Resume'

@pytest.mark.asyncio
async def test_answer_question():
    # Mocking qdrant and RetrievalQA behavior
    with patch('your_module.qdrant.from_documents') as mock_from_documents:
        with patch('your_module.RetrievalQA.from_chain_type') as mock_from_chain_type:
            mock_from_chain_type.return_value.invoke.return_value = {"result": "Test answer"}
            docs = [{'page_content': 'Ernest Hemingway Resume'}]
            question = "What did Ernest Hemingway publish?"
            answer = answer_question(docs, question)
            assert answer == "Test answer"

def test_query_resume():
    # Mocking the whole answer_question function
    with patch('your_module.answer_question', return_value="Mocked answer") as mock_answer_question:
        response = client.get("/query_resume?question=On what page of Hemmingway's resume is his professional experience?")
        assert response.status_code == 200
        assert response.json() == "Mocked answer"