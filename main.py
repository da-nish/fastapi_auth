
from fastapi import FastAPI

app = FastAPI(
    title="My FastAPI Project",
    description="My first FastAPI application",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Welcome to FastAPI!"}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
