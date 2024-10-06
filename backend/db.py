import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://mycroft2003:vf0U4jiUgmDePo1h@sana.7hh2u.mongodb.net/?retryWrites=true&w=majority&appName=Sana"


# Create a new client and connect to the server
def get_client():
    client = MongoClient(uri, server_api=ServerApi("1"), tlsCAFile=certifi.where())
    return client
