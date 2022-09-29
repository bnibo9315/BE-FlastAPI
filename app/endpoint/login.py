from fastapi import APIRouter, Body
from database.connect import connectCollection
import model.response as Response
import model.controller.logincontroller as Logincontroller
from fastapi.encoders import jsonable_encoder

router = APIRouter()



@router.post('/api/login', responses=Response.responsejsonLogin)
async def login(token: str = None, loginData :  Logincontroller.LoginUser = Body()):
    loginData = jsonable_encoder(loginData)
    userCollection = await connectCollection("user")
    tokenLogin = await Logincontroller.loginController(userCollection, loginData)
    return tokenLogin
