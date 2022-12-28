"""Api to communicate with elasticsearch, metarank and final user."""

import os
from typing import List

from app.models.item import Item

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse

from redis import Redis


app: FastAPI = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)
redis_client: Redis = Redis(
    host=os.environ["REDIS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    db=0,
)


@app.get("/")
def get_root() -> HTMLResponse:
    """Get root index.

    Returns:
        HtmlResponse: index page
    """
    with open("./public/index.html") as reader:
        content = reader.read()
    return HTMLResponse(content=content)


@app.post("/item")
def set_item(inputs: Item) -> JSONResponse:
    """Add a new item in the db.

    Returns:
        JSONResponse: Output result.
    """
    redis_client.set(
        name=inputs.name,
        value=inputs.value,
    )
    content: dict = {
        "status_code": 200,
    }
    return JSONResponse(content=content)


@app.post("/items")
def set_items(inputs: List[Item]) -> JSONResponse:
    """Add a new item in the db.

    Returns:
        JSONResponse: Output result.
    """
    for input_ in inputs:
        redis_client.set(
            name=input_.name,
            value=input_.value,
        )

    content: dict = {
        "status_code": 200,
    }
    return JSONResponse(content=content)


@app.get("/item")
def get_item(inputs: str) -> JSONResponse:
    """Add a new item in the db.

    Returns:
        JSONResponse: Output result.
    """
    value = redis_client.get(
        name=inputs,
    ).decode("utf-8")
    content: dict = {
        "value": value,
        "status_code": 200,
    }
    return JSONResponse(content=content)


@app.post("/items")
def get_items(inputs: List[str]) -> JSONResponse:
    """Add a new item in the db.

    Returns:
        JSONResponse: Output result.
    """
    values = [redis_client.get(name=input_).decode("utf-8") for input_ in inputs]
    content: dict = {
        "values": values,
        "status_code": 200,
    }
    return JSONResponse(content=content)
