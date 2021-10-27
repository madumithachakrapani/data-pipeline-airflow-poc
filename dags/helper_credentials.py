import http.client
import json
from pymongo import MongoClient
import pymongo

def insert_credentials():

    data = {
        "key": "LOGIN_CREDENTIALS",
        "SPOTIFY_AUTH": "BQD25fJ2hNB_rYTXi2eXyELjziJf9bHFr5R5rjJyWYK49G9TZexJm0AZ8V6Ug6_ZtQkoAURfSsBVsSqLTMs-FTri7-_MQMz-IqIE8AorGvv9K3I0c3Y2vMMxZ-4KDto8wmzI3OSF1FAdEfTtk5gC5npvRLlIoZjP47uGbY0N",
        "GOOGLE_DRIVE_AUTH": "ya29.a0ARrdaM9gpQis0mmLpYNO5Ls50IiOxZ8uaTgQcdLDmksLyDd6dk30KaHBOGi8p-YQA7VyqMOElZcow0yUnQKVOqjY9cdkC01vAOOxzHABpyx97ajKBCzmKeFxUfIE3aP2PtWsBzD_szmscYZE1kSQZ864bpS-"
    }
    """
    data = {
        "key": "LOGIN_CREDENTIALS",
        "SPOTIFY_AUTH": "BQBLBg0QOfeu1wUtiV4NLvHu9c0M4xD0kv2i3rHNMO0V0xHmwmcNokZwMhU4679yZcQdjecwWWvj0im3mokVlgIIzZJRuWkupmVV3naKbzedq5OsNvQY7MX0I0BjkQMcz7Ayw4GKfVoMajmA3zyglCAgnADESQbtuHqx2w3c",
        "GOOGLE_DRIVE_AUTH": "TjkxOEDudOykeJ1A0H-X1Tioa6YPWegySVFxCl1H61H62nD7NfEL5betFt2YaYOYUZRhYzEqGvbB8ct0ZG4KfHfTBBVvskZPkk2fmbPK5fwq30LjWzh-dUt9z4KP-82aqv7YMFGyV_nTPh8"
    }
    """
    clust = MongoClient("mongodb+srv://gaspricedbuser:gaspricedbuser@cluster0.doq9p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs='CERT_NONE')
    db = clust["MYSPOTIFY"]
    table = db["CREDENTIALS"]
    table.delete_many({})
    table.insert_one(data)

def get_credentials(auth_key):
    clust = MongoClient("mongodb+srv://gaspricedbuser:gaspricedbuser@cluster0.doq9p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs='CERT_NONE')
    db = clust["MYSPOTIFY"]
    table = db["CREDENTIALS"]
    queryResult = table.find({"key":"LOGIN_CREDENTIALS"})

    if auth_key == "GOOGLE_DRIVE_AUTH":
        return "Bearer " + str(queryResult[0][auth_key])
    else:
        return str(queryResult[0][auth_key])

insert_credentials()