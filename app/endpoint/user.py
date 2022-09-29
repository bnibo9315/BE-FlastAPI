from fastapi import APIRouter, Body, HTTPException
from database.connect import connectCollection
import model.response as Response
from model.user import CreateUser, UpdateUser, ChangePassword, getUser, createUser, updateUser, changePassword
from fastapi.encoders import jsonable_encoder
import model.controller.token as Token
from dotenv import load_dotenv
import os
from model.response import ErrorResponseModel
load_dotenv()

router = APIRouter()
key_admin = os.getenv('KEY_ADMIN')


@router.get("/api/users/{id}&token={token}", responses=Response.responsejsonInforuser)
async def get_user(id: str, token: str = None):
    userCollection = await connectCollection("user")
    check_token = await Token.check_token(userCollection,id,token)
    if check_token:
        new_token = Token.refresh_token(token)
        userInfor = await getUser(userCollection, id)
        return userInfor
    message = "Token is expired"
    return ErrorResponseModel(404, message)


@router.post('/api/createusers&token={token}', responses=Response.responsejsonCreateUser)
async def create_user(token: str , inforuser:  CreateUser = Body()):
    check_token = Token.check_token(token)
    if check_token:
        inforuser = jsonable_encoder(inforuser)
        userCollection = await connectCollection("user")
        newuser = await createUser(userCollection, inforuser)
        return newuser
    message = "Token is expired"
    return ErrorResponseModel(404, message)

@router.post('/api/createadmin&token={token}', responses=Response.responsejsonCreateUser)
async def create_admin(token: str, inforuser:  CreateUser = Body()):
    if token == key_admin:
        inforuser = jsonable_encoder(inforuser)
        userCollection = await connectCollection("user")
        newuser = await createUser(userCollection, inforuser)
        return newuser
    message = "Token is vaild. Please contact the administrator"
    return ErrorResponseModel(404, message)

@router.post('/api/updateuser/{id}&token={token}', responses=Response.responsejsonUpdateUser)
async def update_user(id: str, token: str = None, inforuser:  UpdateUser = Body()):
    check_token = Token.check_token(token)
    if check_token:
        inforuser = jsonable_encoder(inforuser)
        userCollection = await connectCollection("user")
        newuser = await updateUser(userCollection, inforuser, id)
        return newuser
    message = "Token is expired"
    return ErrorResponseModel(404, message)


@router.post('/api/changepassword/{id}&token={token}', responses=Response.responsejsonUpdateUser)
async def change_password(id: str, token: str = None, password: ChangePassword = Body(...)):
    check_token = Token.check_token(token)
    if check_token:
        password = jsonable_encoder(password)
        userCollection = await connectCollection("user")
        newuser = await changePassword(userCollection, password, id)
        return newuser
    message = "Token is expired"
    return ErrorResponseModel(404, message)
