from pymongo import MongoClient
import info

def get_database(database=None):
    # Establish connection through localhost
    # If using a remote connection, pass in the connection URI as a string
    # OR pass in domain string as first parameter, and port number as a number as the second parameter
    # EX: MongoClient("brandon@connectingpersonality.com", 27017)
    
    conn_string = f"mongodb+srv://{info.USERNAME}:{info.PASSWORD}@cluster0.8f9qd4d.mongodb.net/?retryWrites=true&w=majority"
    conn = MongoClient(conn_string)
    # Return the connection with a database specified
    if(database):
        return conn[database]
    else:
        return conn

def get_local_database(database=None):
    conn = MongoClient()
    if(database):
        return conn[database]
    else:
        return conn


if __name__ == "__main__":
    # Pass in a string to get that particular database
    db = get_database("test")
    census_data = db['census_data']
    results = census_data.find({})
    for r in results:
        print(r)
    # Pass in nothing to get the main connection object
    db = get_database()

