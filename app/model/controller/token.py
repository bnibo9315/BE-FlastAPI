from datetime import datetime,timedelta
from pydantic import BaseModel
from typing import Union
import os
import jwt
from jwt import ExpiredSignatureError
from dotenv import load_dotenv
from model.response import userResponse,ErrorResponseModel
from bson.objectid import ObjectId

load_dotenv()
key = os.getenv('SECRET_KEY')
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

async def check_token(user_colletction,id,token):
    find_id = None
    if ObjectId.is_valid(id):
        find_id = user_colletction.find_one({"_id": ObjectId(id)})
    if find_id is not None:
        # new_token = refresh_token(token)
        access_expire_old =  jwt.decode(find_id["access_token"], key, algorithms=algorithm_jwt)
        try:
            decoded_jwt = jwt.decode(token, key, algorithms=algorithm_jwt)
            access_expire_current = int(decoded_jwt.get("exp"))  
            # if int(access_expire_old.get("exp")) - access_expire_current
            
            return True
        except ExpiredSignatureError:
            return False
    return False

def refresh_token(token):
    original_token_decoded = jwt.decode(token,key,  algorithms=algorithm_jwt)   
    original_expires = original_token_decoded["exp"]
    expire = int(round((datetime.utcnow() + timedelta(hours=7,minutes=int(refresh_expires))).timestamp()))
    new_expires_time = int(round(expire - original_expires)/60)
    print(new_expires_time)
    new_expires = datetime.utcnow() + timedelta(minutes=new_expires_time)
    new_token = jwt.encode({"exp": new_expires}, key, algorithm=algorithm_jwt)
    return new_token
    