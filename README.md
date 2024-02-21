# Sixfold Sales Engineer Coding Challenge

Our coding challange for sales engineering is a self-directed project. Your task is to implement a simple web service that answers a natural language question based on the contents of a document.

Somebody who can make the right level of impact quickly in this job ought to be able to turn in a solution that works, if not production ready, in 2-3 hours.

## Project environment

Your project must be written in [Python](https://www.python.org/) version 3. Its dependencies must be managed with [Poetry](https://python-poetry.org/).

We have given you a head start!

- The repository defines a Poetry project that declares a few basic dependencies.
- We included a `bin/dev` script that simplifies the process of starting up your service.
- We bootstrapped your service by incorporating a [FastAPI](https://fastapi.tiangolo.com/) server and providing a "hello world" endpoint as a starting point.
- We provided a unit test that exercises the hello world endpoint.

## Functional requirements

Your solution to the challenge must meet the following requirements:

- The service must ingest a PDF document, chunk its text content into pages, create vector embeddings of the pages, and store them in a vector database.
- The service must provide an API endpoint that takes a question written in natural language as a query parameter and responds with an answer to the question.
- The service must use [LangChain](https://langchain.com/) to find the three pages of the PDF that are most similar to the question and prompt an LLM to answer the question using only the content from the best-matching pages.

## Testing requirements

- You must write at least one unit test and one integration test _in addition_ to the test that was provided.

## Documentation requirements

- You must delete these instructions from this document and fashion it into a proper README for your project, explaining how to set up the project, run the tests, and interact with the service.
- The README must also describe any known issues with your solution.

## ChatGPT

We know that it’s super tempting to use ChatGPT for help with coding challenges like this. We’re okay if you do that. This is the distant future, and AIs help us write code all the time!

We just ask that you do a few things:

1. **Just tell us!** We’d love to understand how ChatGPT made this exercise easier for you.
2. **Share your prompts.** This is an opportunity to show us how amazing you are at prompt engineering!
3. **Show us a code diff** of the changes you made to whatever came out of the AI. Be transparent about what you did yourself and what was generated for you.

## Submitting your solution

Do your work on a branch. When you’re ready to submit, open a pull request to the `main` branch. It will automatically be assigned to us for review.

---

## Setup instructions

### Install project dependencies

```
poetry install
# anything else you'd like us to do to get the project running
```

### Copy and update the .env file

```
cp .env.example .env
# anything else you'd like us to do to get the project running
```

## Running
To run the service:
```
bin/dev
```
