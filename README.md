
# You Don't Know Hemmingway

![Alt text](./You%20don't%20know%20Hemmingway.jpg)

Welcome to "You Don't Know Hemmingway," an innovative application designed to delve deep into the professional life of one of the most enigmatic literary figures, Ernest Hemingway. This project is more than just a resume analyzer; it's an interactive experience that invites you to ask questions and explore the fascinating career of Hemingway in a way that's engaging, informative, and, above all, fun.

## About the Project

"You Don't Know Hemmingway" stands at the intersection of literature and technology, offering users a unique platform to inquire about Hemingway's resume. Whether you're curious about his publications, his experiences as a journalist, or his adventures across the globe, this application leverages state-of-the-art technologies to fetch and provide answers:

- **FastAPI**: Powers the backend, ensuring high performance and easy scalability, all with automatic interactive API documentation.
- **OpenAI**: Utilizes cutting-edge AI models for understanding natural language queries and generating informative, accurate responses.
- **Qdrant**: Leverages this vector search engine to efficiently organize and retrieve Hemingway's career highlights based on semantic similarity.
- **Langchain**: Integrates various language AI tools and models, facilitating a seamless interaction between the user's queries and the underlying data processing mechanisms.

## The Journey

This project is a testament to Jason Tissera's relentless pursuit of knowledge and excellence. Initiated as a challenge by Sixfold, "You Don't Know Hemmingway" became Jason's arena to dive headfirst into uncharted technological waters. Despite having no prior experience with FastAPI, OpenAI, Qdrant, or Langchain, Jason embraced the learning curve with focus and determination. The result is an application that not only demonstrates his technical prowess but also his capacity to innovate and inspire.

## Setup Instructions

### Install Dependencies with Poetry
- **Poetry**: Manages dependencies. Install from [here](https://python-poetry.org/).
  - Install dependencies: `poetry install`

### Setup Qdrant with Docker
- **Qdrant**: Requires Docker. Install Docker [here](https://docs.docker.com/engine/install/).
  - Start Qdrant: 
    ```
    docker run -p 6333:6333 -p 6334:6334 \
        -v $(pwd)/qdrant_storage:/qdrant/storage:z \
        qdrant/qdrant
    ```

### Configure OpenAI API
- **OpenAI**: You Don't Know Ernest uses OpenAI's LLM. Obtain an API key [here](https://openai.com/api/).
  - Set API key: 
    ```
    export OPENAI_API_KEY="YOUR_KEY"
    ```

### Start "You don't know Hemmingway"
    
- **Start Service**:
    ```
    bin/dev
    ```

- **Ask your question**:
    Navigate to your service in your browser
    For example: http://[127.0.0.1:8000]/docs#

    For example, you can ask about Hemmingway's resume to understand how the Resume PDF was stored in Qdrant and retrieved.
    ```
    On what page of Hemmingway's resume is his professional experience?
    ```
