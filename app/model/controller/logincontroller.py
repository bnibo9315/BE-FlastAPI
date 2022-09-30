from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timedelta
from model.controller.token import create_access_token, create_refresh_token, insert_token
from passlib.context import CryptContext
from model.response import userResponse, ErrorResponseModel
import os
from dotenv import load_dotenv

load_dotenv()
expires = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
rt_expires = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")


class LoginUser(BaseModel):
    username: str = Field(..., title="Used to login to webstie")
    password: str = Field(..., title="Password to login account")

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "5fec2c0b348df9f22156cc07",
            }
        }


def verify_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


async def loginController(user_colletction, data):
    check_username = user_colletction.find_one({"username": data["username"]})
    if check_username is not None:
        check_password = verify_password(
            data["password"], check_username["password"])
        if check_password:
            message = "Login successfully"
            token = create_access_token(
                {"acc": str(check_username["_id"])}, expires_delta=timedelta(minutes=int(expires)))
            refresh_token = create_refresh_token({"acc": str(
                check_username["_id"])}, expires_delta=timedelta(minutes=int(rt_expires)))
            data_token_save = {
                "_id" : check_username["_id"],
                "access_token" : token.decode(),
                "refresh_token": refresh_token.decode()
            }
            token_save = await insert_token(data_token_save,True)
            if token_save:
                data_token_save.update(
                    {
                        "_id" : str(check_username["_id"])
                    }
                )
                data_token_save.pop("refresh_token")
                return userResponse(data_token_save, message)
            message = "Token is vaild. Please try again later."
        else:
            message = "Password is incorrect"
    else:
        message = "Username does not exist"
    return ErrorResponseModel(404, message)
