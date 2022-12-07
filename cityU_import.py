import json
from pymongo import MongoClient
import os

db_name = "ctuDB"
collection_name = "ctu"
client = MongoClient('localhost', 27017)
db = client[db_name]
collection = db[collection_name]
filenames = os.listdir(
    './data/')
print(filenames)
for filename in filenames:
    os.system(
        'mongoimport --host localhost --port 27017 --collection ' + collection_name + ' --db ' + db_name + ' --jsonArray ./data/'+filename)
client.close()
