from datetime import datetime
import string
from pydantic import BaseModel
from typing import Union

class  InforUser (BaseModel):
    id : int 
    username : str
    fullname : Union[str , None] = None
    email : Union[ str , None] = None
    create : datetime
    modifiled : datetime
    permission : int
    

     