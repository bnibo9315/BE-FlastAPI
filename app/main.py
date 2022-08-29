from __init__ import responseJson,title
from typing import Union
import uvicorn
from fastapi import FastAPI
app = FastAPI(title)



@app.get("/")
def index():
    return responseJson("Ok")



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)