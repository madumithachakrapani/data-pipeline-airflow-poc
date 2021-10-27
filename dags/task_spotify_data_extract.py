import pandas as pd
import requests
import json
from datetime import datetime
import datetime
from helper_credentials import get_credentials

def run_spotify_etl(runID, executionDate):
    TOKEN = get_credentials("SPOTIFY_AUTH")
    # Extract part of the ETL process
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    # Convert time to Unix timestamp in miliseconds
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers = headers)

    print("Calling Spotify API")
    data = r.json()
    print("Printing Spotify response")
    print(data)
    #print(data)

    song_names = []
    # Extracting only the relevant bits of data from the json object
    if "items" in data:
        for song in data["items"]:
            song_item = {
                "song_name" : song["track"]["name"],
                "artist_name" : song["track"]["album"]["artists"][0]["name"],
                "played_at" : song["played_at"],
                "date" : song["played_at"][0:10]
            }
            song_names.append(song_item)

    transformed_data = {
        "runID" : runID,
        "executionDate": executionDate,
        "songs" : song_names
    }
    return transformed_data
