from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "email": "sample@gmail.com",
                "password": "samplepass123",
            }
        }
