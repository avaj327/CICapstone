from pymongo_get_database import get_database
import json
# Load database info
db = get_database("test")
# Upload to census2 to preserve
# original data
collection = db['census_data2']
# Open our finished json file
with open("updated_data_df.json","r") as file:
    json_data = json.load(file)
# print(json_data[0])
collection.insert_many(json_data)