from fastapi import APIRouter, Body, Request
from database.connect import connectCollection
import model.response as Response
from model.user import CreateUser,InforUser, UpdateUser, ChangePassword, getUser, createUser, updateUser, changePassword, findID,deleteUser
from fastapi.encoders import jsonable_encoder
import model.controller.token as Token
from dotenv import load_dotenv
import os
from model.response import ErrorResponseModel
load_dotenv()

router = APIRouter()
key_admin = os.getenv('KEY_ADMIN')


@router.get("/api/users/{id}", responses=Response.responsejsonInforuser)
async def get_user(id: str, token: Request):
    token = token.headers.get('Authorization')
    if token is not None:
        find_id = await findID(id)
        if find_id:
            check_token_vaild = await Token.check_token(id, token)
            if check_token_vaild:
                userInfor = await getUser(id, check_token_vaild[1])
                return userInfor
            message = "Token is expired"
            return ErrorResponseModel(404, message)
        else:
            message = "ID not found"
    else:
        message = "Token not found"
    return ErrorResponseModel(404, message)


@router.post('/api/createusers/{id}', responses=Response.responsejsonCreateUser)
async def create_user(id: str, token: Request, inforuser:  CreateUser = Body()):
    token = token.headers.get('Authorization')
    if token is not None:
        check_token_vaild = await Token.check_token(id, token)
        if check_token_vaild:
            inforuser = jsonable_encoder(inforuser)
            newuser = await createUser(inforuser, check_token_vaild[1])
            return newuser
        message = "Token is expired"
        return ErrorResponseModel(403, message)
    message = "Token not found"
    return ErrorResponseModel(404, message)


@router.post('/api/createadmin', responses=Response.responsejsonCreateUser)
async def create_admin(token: Request, inforuser:  CreateUser = Body()):
    token = token.headers.get('Authorization')
    if token == key_admin:
        inforuser = jsonable_encoder(inforuser)
        newuser = await createUser(inforuser, token)
        return newuser
    message = "Token is vaild. Please contact the administrator"
    return ErrorResponseModel(404, message)


@router.post('/api/updateuser/{id}', responses=Response.responsejsonUpdateUser)
async def update_user(id: str, token: Request, inforuser:  UpdateUser = Body()):
    token = token.headers.get('Authorization')
    if token is not None:
        find_id = await findID(id)
        if find_id:
            check_token_vaild = await Token.check_token(id, token)
            if check_token_vaild:
                inforuser = jsonable_encoder(inforuser)
                newuser = await updateUser(inforuser, id, check_token_vaild[1])
                return newuser
            message = "Token is expired"
            return ErrorResponseModel(403, message)
        else:
            message = "ID not found"
    else:
        message = "Token not found"
    return ErrorResponseModel(404, message)


@router.post('/api/changepassword/{id}', responses=Response.responsejsonUpdateUser)
async def change_password(id: str, token: Request, password: ChangePassword = Body(...)):
    token = token.headers.get('Authorization')
    if token is not None:
        find_id = await findID(id)
        if find_id:
            check_token_vaild = await Token.check_token(id,token)
            if check_token_vaild:
                password_data = jsonable_encoder(password)
                newuser = await changePassword(password_data, id, check_token_vaild[1])
                return newuser
            message = "Token is expired"
            return ErrorResponseModel(404, message)
        else:
            message = "ID not found"
    else:
        message = "Token not found"
    return ErrorResponseModel(404, message)

@router.delete('/api/deteleuser/{id}', responses=Response.responsejsonAction)
async def delete_user(id: str, token: Request , id_delete : InforUser = Body(...)):
    token = token.headers.get('Authorization')
    if token is not None:
        find_id = await findID(id)
        if find_id:
            check_token_vaild = await Token.check_token(id,token)
            if check_token_vaild:
                id_data = jsonable_encoder(id_delete)
                action_status = await deleteUser( id_data, check_token_vaild[1])
                return action_status
            message = "Token is expired"
            return ErrorResponseModel(404, message)
        else:
            message = "ID not found"
    else:
        message = "Token not found"
    return ErrorResponseModel(404, message)