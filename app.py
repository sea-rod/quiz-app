from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from quiz_utils.utils.vector_operations import VectorDBOperations as db
from quiz_utils.generate_questions import generate_questions
from fastapi.middleware.cors import CORSMiddleware
from router import user,file_op

app = FastAPI()

app.include_router(user.router)
app.include_router(file_op.router)

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

