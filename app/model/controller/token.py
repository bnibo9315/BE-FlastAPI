from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Union
import os
import jwt
from jwt import ExpiredSignatureError
from dotenv import load_dotenv
from model.response import userResponse, ErrorResponseModel
from bson.objectid import ObjectId
from database.connect import connectCollection

load_dotenv()
key = os.getenv('SECRET_KEY')
key_rt = os.getenv('SECRET_KEY_RT')
algorithm_jwt = os.getenv('ALGORITHM')
access_expire = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
refresh_expires = os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm_jwt)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(refresh_expires))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key_rt, algorithm=algorithm_jwt)
    return encoded_jwt


async def check_token(id: str, token: str):
    tokenCollection = await connectCollection("token")
    try:
        find_id = tokenCollection.find_one({"_id": ObjectId(id)})
        if find_id is not None and token == find_id["access_token"]:
            if check_token_expries(token):
                return True,token
            elif check_refresh_token_expries(find_id["refresh_token"]):
                new_token = create_access_token(
                    {"acc": id}, expires_delta=timedelta(minutes=int(access_expire)))
                new_refresh_token = create_refresh_token(
                    {"acc": id}, expires_delta=timedelta(minutes=int(refresh_expires)))
                new_data_token_save = {
                    "_id": ObjectId(id),
                    "access_token": new_token.decode(),
                    "refresh_token": new_refresh_token.decode(),
                }
                print("ACCESS_TOKEN is expired. Create new token")
                await insert_token(new_data_token_save)
                return True,new_data_token_save["access_token"]
            else:
                print("REFRESH_TOKEN is expired")
                return False
    except Exception as e:
        print(e)
        return False


def check_token_expries(token):
    try:
        decoded_jwt = jwt.decode(token, key, algorithms=algorithm_jwt)
        return True
    except ExpiredSignatureError:
        return False


def check_refresh_token_expries(token):
    try:
        decoded_jwt = jwt.decode(token, key_rt, algorithms=algorithm_jwt)
        return True
    except ExpiredSignatureError:
        return False


def refresh_token(token):
    original_token_decoded = jwt.decode(token, key,  algorithms=algorithm_jwt)
    original_expires = original_token_decoded["exp"]
    expire = int(round((datetime.utcnow() + timedelta(hours=7,
                                                      minutes=int(refresh_expires))).timestamp()))
    new_expires_time = int(round(expire - original_expires)/60)
    print(new_expires_time)
    new_expires = datetime.utcnow() + timedelta(minutes=new_expires_time)
    new_token = jwt.encode({"exp": new_expires}, key, algorithm=algorithm_jwt)
    return new_token


async def insert_token(data, stauts_login: bool = False):
    tokenCollection = await connectCollection("token")
    userCollection = await connectCollection("user")
    try:
        find_id = userCollection.find_one({"_id": data["_id"]})
        ac_expires_decode = jwt.decode(
            data["access_token"], key,  algorithms=algorithm_jwt)
        rt_expires_decode = jwt.decode(
            data["refresh_token"], key_rt,  algorithms=algorithm_jwt)
        if find_id is None:
            data_token = {
                "_id": data["_id"],
                "access_token": data["access_token"],
                "refresh_token": data["refresh_token"],
                "ac_expires": ac_expires_decode["exp"],
                "rt_expires": rt_expires_decode["exp"],
                "login_at": datetime.now() ,
                "create_at": datetime.now() ,
            }
            insertToken = tokenCollection.insert_one(data_token)
        else:
            data_token = {
                "access_token": data["access_token"],
                "refresh_token": data["refresh_token"],
                "ac_expires": ac_expires_decode["exp"],
                "rt_expires": rt_expires_decode["exp"],
                "modified_at": datetime.now() ,
            }
            if stauts_login:
                data_token.update({
                    "login_at": datetime.now()
                })
            updateToken = tokenCollection.update_one(
                {"_id": data["_id"]}, {"$set": data_token})
        return True
    except Exception as e:
        return False
