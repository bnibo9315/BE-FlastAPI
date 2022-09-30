from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Union
from bson.objectid import ObjectId
from sqlalchemy import delete
from model.response import userResponse, ErrorResponseModel
from passlib.context import CryptContext
from model.controller.logincontroller import verify_password
from database.connect import connectCollection


class InforUser (BaseModel):
    id: str = Field(...,
                    title="Identifier of the user in the system by random numbers.")

    class Config:
        schema_extra = {
            "example": {
                "id": "5fec2c0b348df9f22156cc07",
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


async def findID(id: str):
    data_find = None
    if ObjectId.is_valid(id):
        userCollection = await connectCollection("user")
        data_find = userCollection.find_one(
            {"_id": ObjectId(id)})
    if data_find is not None:
        return True
    return False


async def getUser(id: str, token: str) -> dict:
    data_response = await findID(id)
    if data_response:
        userCollection = await connectCollection("user")
        data_response = userCollection.find_one(
            {"_id": ObjectId(id)})
        message = "Get user information success"
        data = {
            "username": data_response["username"],
            "fullname": data_response["fullname"],
            "email": data_response["email"],
            "create": data_response["create"],
            "modified": data_response["modified"],
            "permisson": data_response["permisson"],
            "_token": token
        }
        return userResponse(data, message)
    message = ({"data": "ID not found", "token": token})
    return ErrorResponseModel(404, message)


async def createUser(data: dict, token: str) -> dict:
    dataCreate = {
        "_id": ObjectId(),
        "create": datetime.now(),
        "modified": datetime.now(),
    }
    userCollection = await connectCollection("user")

    check_username = userCollection.find_one({"username": data["username"]})

    if check_username is None:
        data.update(dataCreate)
        data["password"] = pwd_context.hash(data["password"])
        userCreated = userCollection.insert_one(data)
        if userCreated:
            message = "Create user information success"
            dataCreate["_id"] = str(dataCreate["_id"])
            dataCreate.update({
                "_token": token
            })
            return userResponse(dataCreate, message)
        else:
            message = (
                {"data": "Create user information false", "_token": token})
    else:
        message = ({"data": "Username already exists", "_token": token})
    return ErrorResponseModel(404, message)


async def updateUser(data: dict, id, token: str) -> dict:
    dataUpdate = {
        "modified": datetime.now()
    }
    find_id = await findID(id)
    if find_id:
        data.update(dataUpdate)
        userCollection = await connectCollection("user")
        check_username = userCollection.count({"username": data["username"]})
        if check_username == 0:
            userCreated = userCollection.update_one(
                {"_id": ObjectId(id)}, {"$set": data})
            if userCreated:
                message = "Update user information success"
                dataUpdate.update({"_id": id, "_token": token})
                return userResponse(dataUpdate, message)
        else:
            message = ({"data": "Username already exists", "_token": token})

    else:
        message = ({"data": "ID not found", "token": token})
    return ErrorResponseModel(404, message)


async def changePassword(data: dict, id, token: str) -> dict:
    dataUpdate = {
        "password": pwd_context.hash(data["passnew"]),
        "modified": datetime.now()
    }
    find_id = await findID(id)
    if find_id:
        userCollection = await connectCollection("user")
        check_id = userCollection.find_one({"_id": ObjectId(id)})
        check_password = verify_password(data["passold"], check_id["password"])
        if check_password:
            userCollection = await connectCollection("user")
            userCreated = userCollection.update_one(
                {"_id": ObjectId(id)}, {"$set": dataUpdate})
            if userCreated:
                message = "Update user information success"
                dataUpdate.update({"_id": id, "_token": token})
                dataUpdate.pop("password")
                return userResponse(dataUpdate, message)
            else:
                message = "Update user information false"
        else:
            message = "Password old is incorrect"
    else:
        message = ({"data": "ID not found", "token": token})
    return ErrorResponseModel(404, message)

async def deleteUser(data: dict, token: str) -> dict:
    data_response = await findID(data["id"])
    if data_response:
        userCollection = await connectCollection("user")
        data_response = userCollection.delete_one(
            {"_id": ObjectId(data["id"])})
        message = "Delete user success"
        data = {
            "_token": token
        }
        return userResponse(data, message)
    message = ({"data": "ID not found", "token": token})
    return ErrorResponseModel(404, message)
