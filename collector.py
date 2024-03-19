import requests
from pymongo import MongoClient
import os
import json
import time
import random
from newsapi import NewsApiClient

source = os.getenv('SOURCE', 'newsapi')  # Default to 'gnews'
keyword = os.getenv('KEYWORD', '')
from_date = os.getenv('FROM', '')
to_date = os.getenv('TO', '')
apikey = os.getenv('APIKEY', 'c14142ee09054d3bbbb550eb004d90ed')

client = MongoClient('mongodb://mongo1:27017,mongo2:27018,mongo3:27019/?replicaSet=rs0')
db = client['newsDB']
collection = db[source]

# Base URLs for the APIs
api_urls = {
    'gnews': 'https://gnews.io/api/v4/search',
    'newsapi': 'https://newsapi.org/v2/everything'
}

# Function to fetch articles from GNews
def fetch_from_gnews(keyword, from_date, to_date, apikey):
    response = requests.get(api_urls['gnews'], params={'q': keyword, 'from': from_date, 'to': to_date, 'token': apikey, 'lang': 'en', 'max': 100})
    return response.json()['articles']

# Function to fetch articles from NewsAPI
def fetch_from_newsapi(keyword='', from_date='', to_date='', client=None, page = 1):
    try:
        if keyword == '' and from_date == '' and to_date == '':
            articles = client.get_everything(language='en', page_size=100, page=page)
        elif from_date == '' and to_date == '':
            articles = client.get_everything(q=keyword, language='en', sort_by='relevancy', page_size=100, page=page)
        elif keyword == '':
            articles = client.get_everything(from_param=from_date, to=to_date, language='en', sort_by='relevancy', page_size=100, page=page)
        else:
            articles = client.get_everything(q=keyword, from_param=from_date, to=to_date, language='en', sort_by='relevancy', page_size=100, page=page)
        return articles['articles']
    except Exception as e:
        print(f'API Limit reached, waiting for 1 day')
        time.sleep(86400)
        return None

def insert_to_mongo(articles):
    print('\n--- Inserting articles to MongoDB ---\n')
    try:
        # check if the article already exists in the database
        removed = 0
        for article in articles:
            if collection.find_one({'url': article['url']}):
                articles.remove(article)
                removed += 1
        if removed > 0:
            print(f'Removed {removed} duplicate articles')
        if removed == len(articles):
            print('No new articles to insert')
            return
        if len(articles) == 0:
            print('No new articles to insert')
            return
        collection.insert_many(articles)
        print(f'Inserted {len(articles)} articles to MongoDB')
    except Exception as e:
        print(f'Error: {e}')

# Main function to decide which source to use and print results
def main():
    page = 1
    while True:
        articles = []
        if source.lower() == 'gnews':
            articles = fetch_from_gnews(keyword, from_date, to_date, apikey)
            insert_to_mongo(articles)
        elif source.lower() == 'newsapi':
            news_api_client = NewsApiClient(api_key=apikey)
            articles = fetch_from_newsapi(keyword, from_date, to_date, client=news_api_client, page=page)
            if articles is None:
                print('API limit reached, waiting for 1 day')
                time.sleep(86400)
            else:
                page += 1
                print(f'Fetched page {page} from NewsAPI')
                insert_to_mongo(articles)

        else:
            print('Invalid source')
            return
        

if __name__ == '__main__':
    main()
