from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from utils.vector_operations import VectorDBOperations as db
from generate_questions import generate_questions

app = FastAPI()


@app.get("/")
def read_root():
    client= db.connect_weaviate() 
    res = generate_questions(client)
    return StreamingResponse(res)
    # return {"Error": "some error occured"}