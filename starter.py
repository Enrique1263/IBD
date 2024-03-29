import pymongo

# MongoDB connection string
connection_string = 'mongodb://mongo1:27017,mongo2:27018,mongo3:27019/?replicaSet=rs0'

# Connecting to MongoDB
client = pymongo.MongoClient(connection_string)

# Database name
db_name = 'newsDB'

# Check if the database exists
dblist = client.list_database_names()
if db_name not in dblist:
    print(f"Database '{db_name}' does not exist. Creating...")
    
    # Creating the database by creating collections since MongoDB creates databases and collections automatically when you first store data in them
    db = client[db_name]
    
    # Collections to be created
    collections = ['gnews', 'newsapi', 'newsai']
    
    for collection in collections:
        db.create_collection(collection)
        print(f"Collection '{collection}' created.")
else:
    print(f"Database '{db_name}' already exists.")

# Closing the connection
client.close()