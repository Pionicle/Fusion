# Import FastAPI to create a web application
from fastapi import FastAPI

# Initialize a new FastAPI application instance
app = FastAPI()


# Define a GET endpoint at the root path ("/") that returns a JSON message
@app.get("/")
def read_root():
    return {"message": "Hello world!"}
