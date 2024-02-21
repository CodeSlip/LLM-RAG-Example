import logging
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Query

logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI()


@app.get("/hello")
def hello(name: Annotated[str, Query()] = "Wilson"):
    return {"message": f"Hello {name}!"}
