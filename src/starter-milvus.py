from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility


# Connecting to Milvus
connections.connect("default", host="milvus-standalone", port="19530")

collection_name = "articles"

# Verify if collection exists
collection_exist = utility.has_collection(collection_name)
if not collection_exist:
    print(f"Collection '{collection_name}' does not exist. Creating...")

    # Collection schema
    fields = [
            FieldSchema(name="url", dtype=DataType.VARCHAR, max_length = 2048, is_primary=True),
            FieldSchema(name="title", dtype=DataType.VARCHAR , max_length = 1024),
            FieldSchema(name="description", dtype=DataType.VARCHAR, max_length = 4096),
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length = 1024),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)
    ]

    schema = CollectionSchema(fields, description="News Articles Collection")
    
    # Creating the collection 
    collection = Collection(name=collection_name, schema=schema)

    index_params = {
        'metric_type': 'COSINE',
        'index_type': "IVF_FLAT",
        'params': {"nlist": 128}
    }
    collection.create_index(field_name='embedding', index_params=index_params)

    print(f"Collection '{collection_name}' created.")
else:
    print(f"Collection '{collection_name}' already exists.")

# Closing the connection
connections.disconnect("default")
