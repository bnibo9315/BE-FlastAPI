from datetime import datetime
from pydantic import BaseModel, Field
from typing import Union
import json
import bson.json_util as json_util
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from bson.json_util import dumps, loads
# UserController
responsejsonInforuser = {
    200: {
        "description": "Information user requested by id",
        "content": {
            "application/json": {
                "example": {
                    "status": True,
                    "message": "Get information about users",
                    "code": 200,
                    "data":  {
                        "username": "admin",
                        "fullname": "Admin AI",
                        "email": "admin@gmail.com",
                        "create": 1663838293577,
                        "modified": 1663838293577,
                        "permission": 1
                    }
                }
            }
        },
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "status": False,
                    "message": "ID not found",
                    "code": 422,
                }
            }
        },
    },
}


def userResponse(obj, message : str) -> dict:
    return {
        "status": True,
        "message": message,
        "code": 200,
        "data": obj,
    }


def ErrorResponseModel(code, error):
    return JSONResponse(
            status_code=code,
            content=jsonable_encoder({"status": False, "code": code, "message": error }))

responsejsonCreateUser = {
    200: {
        "description": "Create user using controller action in website",
        "content": {
            "application/json": {
                "example": {
                    "status": True,
                    "message": "Create user successfully",
                    "code": 200,
                    "data":  {
                        "_id": "63313234abc910453f650cdd",
                        "create":"1664193700962",
                        "modified": "1664193700962"
                    }
                }
            }
        },
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "status": False,
                    "message": "Action false. Check data form ",
                    "code": 422,
                    "detail": "abcxyz",
                }
            }
        },
    },
}

responsejsonUpdateUser = {
    200: {
        "description": "Update user using controller action in website",
        "content": {
            "application/json": {
                "example": {
                    "status": True,
                    "message": "Update user successfully",
                    "code": 200,
                    "data":  {
                        "_id": "63313234abc910453f650cdd",
                        "modified": "1664193700962"
                    }
                }
            }
        },
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "status": False,
                    "message": "Action false. Check data form ",
                    "code": 422,
                    "detail": "abcxyz",
                }
            }
        },
    },
}

responsejsonLogin = {
    200: {
        "description": "Login controller in website",
        "content": {
            "application/json": {
                "example": {
                    "status": True,
                    "message": "Create user successfully",
                    "code": 200,
                    "data":  {
                        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJhY2MiOiJhZG1pbiIsImV4cCI6MTY2NDQyMTM3OX0.Sh_CjPLfkAIXhR65Q3DL-czoXiDpHvJRgQR7jBS79NCG3xbban0e_mcCHxk-2n-YkMh9VF9esYGto1L1PRbNOg"
                    }
                }
            }
        },
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "status": False,
                    "message": "Action false. Check data form ",
                    "code": 422,
                    "detail": "abcxyz",
                }
            }
        },
    },
}

responsejsonAction = {
    200: {
        "description": "Login controller in website",
        "content": {
            "application/json": {
                "example": {
                    "status": True,
                    "message": "Create user successfully",
                    "code": 200,
                    "data":  {
                        "data" : "Action successfully",
                        "_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJhY2MiOiJhZG1pbiIsImV4cCI6MTY2NDQyMTM3OX0.Sh_CjPLfkAIXhR65Q3DL-czoXiDpHvJRgQR7jBS79NCG3xbban0e_mcCHxk-2n-YkMh9VF9esYGto1L1PRbNOg"
                    }
                }
            }
        },
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "status": False,
                    "message": "Action false. Check data form ",
                    "code": 422,
                    "detail": "abcxyz",
                }
            }
        },
    },
}