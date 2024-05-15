from pymongo import MongoClient
from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer
from glob import glob
import os
import json


apiname = os.getenv('API_NAME', 'newsapi')

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

folder_name = f'/app/data/{apiname}'

def insert_mongo(docs):
    connection_string = os.getenv('MONGO_CONNECTION_STRING', 'mongodb://mongo1:27017,mongo2:27018,mongo3:27019/?replicaSet=rs0')
    client = MongoClient(connection_string)

    collection_name = 'articles'
    connections.connect("default", host="milvus-standalone", port="19530")
    collection_milvus = Collection(name=collection_name)


    db = client['newsDB']
    collection = db['articles']
    # check if url already exists in collection
    # if not, insert
    for doc in docs:
        if collection.find_one({'url': doc['url']}) is None:
            doc_to_insert = {
                'title': doc['title'],
                'description': doc['description'],
                'content': doc['content'],
                'author': doc['author'],
                'url': doc['url'],
                'source': doc['source'],
            }
            collection.insert_one(doc_to_insert)
            milvus_doc = {
                'url': doc['url'],
                'title': doc['title'],
                'description': doc['description'],
                'source': doc['source'],
                'embedding': doc['embedding']
            }
            
            collection_milvus.insert([milvus_doc])





    client.close()

def insert_milvus(docs):
    # check if embedding already exists in collection
    # if not, insert
    raise NotImplementedError

def process_files(files):
    unprocessed_files = [file for file in files if 'processed' not in file]

    if len(unprocessed_files) == 0:
        return
    
    docs = []

    '''
    structure of docs:
    [
        {
            'title': 'title',
            'description': 'description',
            'content': 'content',
            author: 'author',
            publishedAt: 'publishedAt',
            url: 'url',
            source: 'source',
            'embedding': []
        }
    ]
    '''

    for file in unprocessed_files:
        print(f'Processing {file}')
        with open(file, 'r') as f:
            articles = f.readlines()

        articles = [json.loads(article) for article in articles]

        docs = []

        print(f'Processing {len(articles)} articles')

        if apiname == 'newsapi':

            texts = []
            for article in articles:
                string = f"{article['title']}. {article['description']}. {article['content']}"
                texts.append(string)

            print('Embedding texts')

            embeddings = model.encode(texts)

            print('Formatting articles')

            for i, article in enumerate(articles):
                new_article = {
                    'api': 'newsapi',
                    'title': article['title'],
                    'description': article['description'],
                    'content': article['content'],
                    'author': article['author'],
                    'publishedAt': article['publishedAt'],
                    'url': article['url'],
                    'source': article['source']['name'],
                    'embedding': embeddings[i].tolist()
                }

                docs.append(new_article)
                
 
        elif apiname == 'gnews':
                
            texts = []
            for article in articles:
                string = f"{article['title']}. {article['description']}. {article['content']}"
                texts.append(string)

            print('Embedding texts')

            embeddings = model.encode(texts)

            print('Formatting articles')

            for i, article in enumerate(articles):
                new_article = {
                    'api': 'gnews',
                    'title': article['title'],
                    'description': article['description'],
                    'content': article['content'],
                    'author': article['source']['name'],
                    'publishedAt': article['publishedAt'],
                    'url': article['url'],
                    'source': article['source']['name'],
                    'embedding': embeddings[i].tolist()
                }

                docs.append(new_article)

        elif apiname == 'newsapiai':
                    
            texts = []
            for article in articles:
                string = f"{article['title']}. {article['body']}"
                texts.append(string)

            print('Embedding texts')

            embeddings = model.encode(texts)

            print('Formatting articles')

            for i, article in enumerate(articles):
                new_article = {
                    'api': 'newsapiai',
                    'title': article['title'],
                    'description': article['body'][:100] + '...',
                    'content': article['body'],
                    'author': article['authors'],
                    'publishedAt': article['dateTimePub'],
                    'url': article['url'],
                    'source': article['source']['title'],
                    'embedding': embeddings[i].tolist()
                }

                docs.append(new_article)

        else:
            print('Invalid API name')
            return
        
        print('Writing processed articles to file')

        

        os.rename(file, file.replace('.json', '_processed.json'))

        file_name = r'/app/data/processed/' + file.split('/')[-1]

        with open(file_name, 'w') as f:
            for article in docs:
                json.dump(article, f, default=str)
                f.write('\n')

        print('Inserting articles into database(s)')

        insert_mongo(docs)
        #insert_milvus(docs)


if __name__ == '__main__':
    while True:
        files = glob(f'{folder_name}/*.json')
        process_files(files)





{"title": "Politics watch: Apology to Stardust victims' families, hate speech legislation", 
 "description": "Here, we have a look at the topics likely to dominate political debate in the week to come", 
 "content": "Here, we have a look at the topics likely to dominate political debate in the week to come.\nStardust apology\nThe D\u00e1il returns on Tuesday and Taoiseach Simon Harris will make an official state apology to the families of the victims of the Stardust nig... [1526 chars]", 
 "url": "https://www.breakingnews.ie/ireland/politics-watch-apology-to-stardust-victims-families-hate-speech-legislation-1616600.html", 
 "image": "https://img.resized.co/breaking-news/eyJkYXRhIjoie1widXJsXCI6XCJodHRwczpcXFwvXFxcL2ltYWdlcy5icmVha2luZ25ld3MuaWVcXFwvcHJvZFxcXC91cGxvYWRzXFxcLzIwMjRcXFwvMDRcXFwvMjIyMTAwMzVcXFwvUEEtNzU5MzI0NTgtZTE3MTM4MTYwNTExMDguanBnXCIsXCJ3aWR0aFwiOjEyMDAsXCJoZWlnaHRcIjo2MjcsXCJkZWZhdWx0XCI6XCJodHRwczpcXFwvXFxcL3d3dy5icmVha2luZ25ld3MuaWVcXFwvaW1hZ2VzXFxcL25vLWltYWdlLnBuZ1wiLFwib3B0aW9uc1wiOltdfSIsImhhc2giOiI4ODI5ODI3MWMzMDk2N2JjZmRlZTZiNWY4ZjViMzZhNjQ4MDJhYTcxIn0=/politics-watch-apology-to-stardust-victims-families-hate-speech-legislation.jpg", "publishedAt": "2024-04-21T23:00:00Z", "source": {"name": "BreakingNews.ie", "url": "https://www.breakingnews.ie"}}
