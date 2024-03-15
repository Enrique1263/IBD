import requests
from pymongo import MongoClient
import os
import json
import time
import random

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "newsDB")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "articles")
QUERY = os.environ.get("QUERY")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def fetch_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        print(f"Failed to fetch news: {response.status_code}")
        return []

def insert_news(news):
    time.sleep(random.randint(1, 5))
    for article in news:
        if not collection.find_one({"url": article['url']}):
            collection.insert_one(article)
            print(f"Inserted: {article['title']}")

def main():
    while True:
        news = fetch_news(QUERY)
        if news:
            insert_news(news)
        else:
            print("No news to insert")

if __name__ == "__main__":
    main()