from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Union
from bson.objectid import ObjectId
from model.response import userResponse, ErrorResponseModel
from passlib.context import CryptContext
from model.controller.logincontroller import verify_password

class InforUser (BaseModel):
    id: int = Field(...,
                    title="Identifier of the user in the system by random numbers.")
    token: Union[str, None] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "5fec2c0b348df9f22156cc07",
                "token": "5fec2c0b348df9f22156cc07"
            }
        }


class CreateUser(BaseModel):
    fullname: str = Field(..., title="User's first and last name")
    username: str = Field(..., title="Used to login to webstie")
    email: str = Field(
        None, title="ink your email account to find your account or notify some information", alias="email")
    password: str = Field(..., title="Password to login account")
    permisson: str = Field(..., title="Permissions of users in the system")

    class Config:
        schema_extra = {
            "example": {
                "_id": "6331798e39fb39ab5b21d1e5",
                "fullname": "Nguyen Van A",
                "username": "admin",
                "email": "admin@example.com",
                "permisson": 1
            }
        }


class UpdateUser(BaseModel):
    fullname: str = Field(..., title="User's first and last name")
    username: str = Field(..., title="Used to login to webstie")
    email: str = Field(
        None, title="ink your email account to find your account or notify some information", alias="email")
    permisson: str = Field(..., title="Permissions of users in the system")

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Nguyen Van A",
                "username": "admin",
                "email": "admin@example.com",
                "permisson": 1
            }
        }

class ChangePassword(BaseModel):
    passold: str = Field(..., title="Password old to login account")
    passnew: str = Field(..., title="Password new to login account")

    class Config:
        schema_extra = {
            "example": {
                "passold": "312",
                "passnew": "123"
            }
        }

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def getUser(user_colletction, id: str) -> dict:
    data_response = None
    if ObjectId.is_valid(id):
        data_response = user_colletction.find_one(
            {"_id": ObjectId(id)})
    if data_response is not None:
        message = "Get user information success"
        data = {
            "username": data_response["username"],
            "fullname": data_response["fullname"],
            "email": data_response["email"],
            "create": data_response["create"],
            "modified": data_response["modified"],
            "permisson": data_response["permisson"],
        }
        return userResponse(data, message)
    message = "ID not found"
    return ErrorResponseModel(404, message)


async def createUser(user_colletction, data: dict) -> dict:
    dataCreate = {
        "_id": ObjectId(),
        "create": datetime.now(),
        "modified": datetime.now(),
    }
    check_username = user_colletction.count({"username": data["username"]})

    if check_username == 0:
        data.update(dataCreate)
        data["password"] = pwd_context.hash(data["password"])
        userCreated = user_colletction.insert_one(data)
        if userCreated:
            message = "Create user information success"
            dataCreate["_id"] = str(dataCreate["_id"])
            return userResponse(dataCreate, message)
        else:
            message = "Create user information false"
    else:
        message = "Username already exists"
    return ErrorResponseModel(404, message)


async def updateUser(user_colletction, data: dict,id) -> dict:
    dataUpdate = {
        "modified": datetime.now()
    }
    find_id = None
    if ObjectId.is_valid(id):
        find_id = user_colletction.find_one({"_id": ObjectId(id)})
    if find_id is not None:
        data.update(dataUpdate)
        userCreated =  user_colletction.update_one({"_id": ObjectId(id)}, {"$set": data})
        if userCreated:
            message = "Update user information success"
            dataUpdate.update({"_id": id})
            return userResponse(dataUpdate, message)
        else:
            message = "Update user information false"

    message = "ID not found"
    return ErrorResponseModel(404, message)

async def changePassword(user_colletction, data: dict,id) -> dict:
    dataUpdate = {
        "password": pwd_context.hash(data["passnew"]),
        "modified": datetime.now()
    }
    find_id = None
    if ObjectId.is_valid(id):
        find_id = user_colletction.find_one({"_id": ObjectId(id)})
        message = "ID not found"
    if find_id is not None:
        check_password = verify_password(data["passold"], find_id["password"])
        if check_password :
            data.update(dataUpdate)
            userCreated =  user_colletction.update_one({"_id": ObjectId(id)}, {"$set": data})
            if userCreated:
                message = "Update user information success"
                dataUpdate.update({"_id": id})
                dataUpdate.pop("password")
                return userResponse(dataUpdate, message)
            else:
                message = "Update user information false"
        else:
            message = "Password old is incorrect"

    return ErrorResponseModel(404, message)