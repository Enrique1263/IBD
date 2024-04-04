from pymongo import MongoClient
import json
from datetime import datetime
import os

# MongoDB connection string
# Replace 'your_replica_set_url' with your actual MongoDB replica set URL
# Include the database name in the connection string
connection_string = os.getenv('CONNECTIONSTRING')

# Establish a connection to the MongoDB
client = MongoClient(connection_string)

# Database and collections
db = client.newsDB
collections = ['gnews', 'newsapi', 'newsai']

def extract_and_dump():
    for collection_name in collections:
        collection = db[collection_name]
        # Extract all documents. You might want to modify this to filter documents.
        documents = collection.find({})
        
        # Convert documents to a list of dictionaries
        docs_list = list(documents)
        
        # Dump to JSON file
        file_name = f"./data/{collection_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        with open(file_name, 'w') as file:
            json.dump(docs_list, file, default=str, indent=4)  # Using default=str to handle datetime objects

if __name__ == "__main__":
    extract_and_dump()
