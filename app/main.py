from __init__ import app
import __init__
from typing import Union
from model.user import InforUser 
from model.response import responseJson
import uvicorn
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# @app.post("/",tags=["Index page"],responses= __init__.responsesDetail)
# def index(token: str = Depends(oauth2_scheme)):
#     return responseJson( True, token)

# @app.post("/api/controller/login",response_description="Controller login page -> create a new token is login sucesss")
# async def login(token: str = Depends(oauth2_scheme)):
#     return responseJson( True, token)

@app.get("/api/controller/getusers",response_description="Controller get information about users")
async def getusers():
    return responseJson( True , "Get information about users")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)