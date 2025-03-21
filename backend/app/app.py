from fastapi import FastAPI, Depends
from typing import Annotated
from core.vector_operations import VectorDBOperations as db
from services.generate_questions import generate_question
from fastapi.middleware.cors import CORSMiddleware
from api.v1.router import user, file_op

app = FastAPI()

app.include_router(user.router)
app.include_router(file_op.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/gen_questions")
def gen_questions(user_id: Annotated[str, Depends(file_op.validate_token)]):
    client = db.connect_weaviate()
    res = generate_question(client, user_id)

    return {"questions": res}

