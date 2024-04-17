import os
import datetime
from eventregistry import EventRegistry, QueryArticles, RequestArticlesInfo
import pymongo
import json


def fetch_news_newasai(api_keys, keywords, from_date, to_date, language):
    """
    Fetch articles based on keywords, date range, and language using multiple API keys.

    :param api_keys: List of EventRegistry API keys
    :param keywords: List of keywords to search for
    :param start_date: Start date for the article search (YYYY-MM-DD format)
    :param end_date: End date for the article search (YYYY-MM-DD format)
    :param language: Language code for the articles (e.g., 'eng' for English)
    :return: A list of articles
    """
    CALLS_PER_KEY = int(os.getenv('NEWSAPIAICALLSPERKEY'))
    NUM_KEYS = len(api_keys)
    NUM_TOPICS = len(keywords)
    topics_per_key = NUM_TOPICS // NUM_KEYS # debe ser entera
    calls_per_key_per_topic = CALLS_PER_KEY // topics_per_key 

    if language == 'en':
        language = 'eng'

    if language == 'es':
        language = 'spa'

    
    articles = []
    start_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    
    used_keys = []

    
    i = 0
    
    for topic in keywords:
        er = EventRegistry(apiKey=api_keys[0])
        q = QueryArticles(keywords=topic, 
                        lang=language,
                        dateStart=start_date,
                        dateEnd=end_date,
                        isDuplicateFilter="skipDuplicates"
                        
                        )
        q.setRequestedResult(RequestArticlesInfo(count=calls_per_key_per_topic))
        response = er.execQuery(q)
        if 'articles' in response:
            articles.extend(response['articles']['results']) 
        print(f'Processed {topic}')
        i += 1
        if i % topics_per_key == 0:
            i = 0
            api_keys.append(api_keys.pop(0))
            print('Switching to next API key...')
        
    
    connection_string = os.getenv('CONNECTIONSTRING')
    client = pymongo.MongoClient(connection_string)
    db_name = 'newsDB'
    collection_name = 'newsai'
    col = client[db_name][collection_name]
    if len(articles) == 0:
        print('No articles found')
    else:
        col.insert_many(articles)
        file_name = f"./data/{collection_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        with open(file_name, 'w') as file:
            json.dump(articles, file, default=str, indent=4)
    client.close()

if __name__ == '__main__':
    api_keys = os.getenv('NEWSAPIAIKEY').split(',')
    keywords = os.getenv('NEWSAPIAITOPICS').split(',')
    from_date = os.getenv('FROM')
    to_date = os.getenv('TO')
    language = os.getenv('LANGUAGE')
    fetch_news_newasai(api_keys, keywords, from_date, to_date, language)