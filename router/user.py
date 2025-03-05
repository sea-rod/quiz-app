from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from .schema import User
from fire_auth.firebase_auth import firebase_connect
from firebase_admin import auth
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()
db = firebase_connect()


@router.post("/user/register")
def resigter_user(user: User):
    try:
        user = auth.create_user(email=user.username, password=user.password)

        return JSONResponse(
            content={
                "message": f"User account created successfuly for user {user.uid}"
            },
            status_code=201,
        )
    except auth.EmailAlreadyExistsError as _:
        raise HTTPException(
            status_code=400,
            detail=f"Account already created for the email {user.username}",
        ) from _


# @router.post("/user/login")
# def authenticate(user: User):
#     try:
#         user_ = auth.get_user_by_email(user.username)
#         token = user["idToken"]

#         return JSONResponse(content={"token": token}, status_code=200)

#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Invalid Credentials")


# @router.post("/ping")
def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        print(token)
        user = auth.verify_id_token(token)

        return user["user_id"]
    except auth.ExpiredIdTokenError as e:
        raise HTTPException(status_code=400, detail="Token Expried") from e