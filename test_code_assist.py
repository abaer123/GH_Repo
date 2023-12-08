
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


@app.get("/users/")
def read_users():
    return {"message": "Hello, world!"}


@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"message": "Hello, world!"






