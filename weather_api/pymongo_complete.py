import pymongo
import json
import os 
import mongopass
from mongopass import account

# Connect to client
client = pymongo.MongoClient(account)

# Database name and collection
db_name = 'test'
collection_name = 'weather_data'

# JSON file path
file_path = os.path.expanduser("~/Desktop/capstone_data/all_weather_data.json")

# Loads JSON file
with open(file_path) as file:
    json_data = json.load(file)

# Specific collecton to insert data
collection = client[db_name][collection_name]

# Inserts JSON document into the collection
collection.insert_one(json_data)