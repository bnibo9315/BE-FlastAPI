from __init__ import responseJson,app
import __init__
from typing import Union
import uvicorn
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@app.post("/",tags=["Index page"],responses= __init__.responsesDetail)
def index(token: str = Depends(oauth2_scheme)):
    return responseJson( True, token)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)