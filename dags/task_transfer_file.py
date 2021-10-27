import json
import requests
from helper_credentials import get_credentials

def transfer_file_to_drive(fileName) -> bool:
    TOKEN = get_credentials("GOOGLE_DRIVE_AUTH")
    headers = {"Authorization": TOKEN}
    para = {
        "name": fileName,
        "parents":["1W8PAIQAzoSD_cN7DdihoNZQ70UAFi5vh"]
    }
    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open("spotify_report.csv", "rb")
    }
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
    )

    response=json.loads(r.text)
    #print(response["error"]["code"])
    print(r.text)
    status = False
    if("error" in response):
        status = False
        print("file uploaded failed")
    else:
        status = True
        print("file uploaded success")

    return status