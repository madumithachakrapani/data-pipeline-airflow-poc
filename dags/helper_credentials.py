import http.client
import json
from pymongo import MongoClient
import pymongo

def insert_credentials():

    data = {
        "key": "LOGIN_CREDENTIALS",
        "SPOTIFY_AUTH": "YOUR SPOTIFY CREDENTIALS",
        "GOOGLE_DRIVE_AUTH": "YOUR GOOGLE CREDENTIALS"
    }
    
    clust = MongoClient("YOUR MONGODB CONNECTION STRING", ssl=True,ssl_cert_reqs='CERT_NONE')
    db = clust["MYSPOTIFY"]
    table = db["CREDENTIALS"]
    table.delete_many({})
    table.insert_one(data)

def get_credentials(auth_key):
    clust = MongoClient("YOUR MONGODB CONNECTION STRING", ssl=True,ssl_cert_reqs='CERT_NONE')
    db = clust["MYSPOTIFY"]
    table = db["CREDENTIALS"]
    queryResult = table.find({"key":"LOGIN_CREDENTIALS"})

    if auth_key == "GOOGLE_DRIVE_AUTH":
        return "Bearer " + str(queryResult[0][auth_key])
    else:
        return str(queryResult[0][auth_key])

insert_credentials()
