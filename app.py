from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from quiz_utils.utils.vector_operations import VectorDBOperations as db
from quiz_utils.generate_questions import generate_questions
from fastapi import UploadFile
from fastapi.middleware.cors import CORSMiddleware
import json
from router import user

app = FastAPI()

app.include_router(user.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    client = db.connect_weaviate()
    res = generate_questions(client)
    return StreamingResponse(res)
    # return {"Error": "some error occured"}


@app.post("/uploadfile/")
def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
