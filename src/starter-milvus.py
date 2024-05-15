from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType


# Connecting to Milvus
connections.connect("default", host="milvus-standalone", port="19530")

collection_name = "news_articles"

# Verify if collection exists
if not Collection.exists(collection_name):
    print(f"Collection '{collection_name}' does not exist. Creating...")

    # Collection schema
    fields = [
        FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=512, description="URL of the news article"),
        FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=256, description="Title of the news article"),
        FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=1024, description="Description of the news article")
    ]

    schema = CollectionSchema(fields, description="News Articles Collection")
    
    # Creating the collection 
    collection = Collection(name=collection_name, schema=schema)
    print(f"Collection '{collection_name}' created.")
else:
    print(f"Collection '{collection_name}' already exists.")

# Closing the connection
connections.disconnect("default")
