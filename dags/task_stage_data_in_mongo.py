from pymongo import MongoClient
def store_in_mongo(data):
    print("Printing data in store_in_mongo")
    print(data)

    clust = MongoClient("mongodb+srv://gaspricedbuser:gaspricedbuser@cluster0.doq9p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs='CERT_NONE')
    db = clust["MYSPOTIFY"]
    table = db["SPOTIFYSONGS"]
    table.delete_many({})
    table.insert_one(data)


