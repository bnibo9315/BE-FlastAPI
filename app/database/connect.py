from email.policy import strict
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv('USER_ADMIN')
password = os.getenv('PASS_ADMIN')
dbname = os.getenv('DB_NAME')
hostname = os.getenv('HOST_NAME')
port = int(os.getenv('PORT'))


async def connectCollection(collection: str) -> dict:
    client = MongoClient(host=hostname, port=port, username=username,
                         password=password, authSource=dbname)
    db = client[dbname]
    user_colletction = db[collection]
    return user_colletction
