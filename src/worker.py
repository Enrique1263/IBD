from pymongo import MongoClient
from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer
from glob import glob
import os
import json


apiname = os.getenv('API_NAME', 'newsapi')

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

folder_name = f'/app/data/{apiname}'

def insert_mongo(docs):
    # check if url already exists in collection
    # if not, insert
    raise NotImplementedError

def insert_milvus(docs):
    # check if embedding already exists in collection
    # if not, insert
    raise NotImplementedError

def process_files(files):
    unprocessed_files = [file for file in files if 'processed' not in file]

    if len(unprocessed_files) == 0:
        print('No unprocessed files found')
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
        with open(file, 'r') as f:
            articles = f.readlines()

        articles = [json.loads(article) for article in articles]

        docs = []

        if apiname == 'newsapi':

            texts = []
            for article in articles:
                string = f"{article['title']}. {article['description']}. {article['content']}"
                texts.append(string)

            embeddings = model.encode(texts)

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

            embeddings = model.encode(texts)

            for i, article in enumerate(articles):
                new_article = {
                    'api': 'gnews',
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

        elif apiname == 'newsapiai':
                    
            texts = []
            for article in articles:
                string = f"{article['title']}. {article['body']}"
                texts.append(string)

            embeddings = model.encode(texts)

            for i, article in enumerate(articles):
                new_article = {
                    'api': 'newsapiai',
                    'title': article['title'],
                    'description': article['body'][:100] + '...',
                    'content': article['content'],
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

        

        os.rename(file, file.replace('.json', '_processed.json'))

        with open(f'/app/data/processed/{file}', 'w') as f:
            for article in articles:
                f.write(json.dumps(article) + '\n')

        insert_mongo(docs)
        insert_milvus(docs)


if __name__ == '__main__':
    while True:
        files = glob(f'{folder_name}/*.json')
        process_files(files)





