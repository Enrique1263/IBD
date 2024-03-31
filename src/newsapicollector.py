import os
from dotenv import load_dotenv
import pymongo
from newsapi import NewsApiClient

def fetch_news(api_keys, keywords, from_date, to_date, language):
    connection_string = 'mongodb://mongo1:27017,mongo2:27018,mongo3:27019/?replicaSet=rs0'
    client = pymongo.MongoClient(connection_string)
    db_name = 'newsDB'
    collection_name = 'newsapi'
    col = client[db_name][collection_name]

    newsapi = NewsApiClient(api_key=api_keys[0])
    used_keys = []
    for keyword in keywords:
        if len(used_keys) == len(api_keys):
            print('All API keys used up')
            break
        page = 1
        while True:
            try:
                response = newsapi.get_everything(q=keyword,
                                                from_param=from_date,
                                                to=to_date,
                                                language=language,
                                                page=page)
                if response['status'] == 'ok':
                    articles_to_insert = response['articles']
                    col.insert_many(articles_to_insert)
                    page += 1
            except Exception as e:
                e = dict(e.args[0])
                if e['code'] == 'rateLimited':
                    api_keys.append(api_keys.pop(0))
                    used_keys.append(api_keys[-1])
                    if len(used_keys) == len(api_keys):
                        break
                    else:
                        print('Rate limited, switching to next API key')
                    newsapi = NewsApiClient(api_key=api_keys[0])

                elif e['code'] == 'maximumResultsReached':
                    print('Maximum results reached, changing keyword')
                    break
                else:
                    print('Unknown error: ', e)
                    break
    client.close()

    

if __name__ == '__main__':
    load_dotenv()
    api_keys = os.getenv('NEWSAPIKEY').split(',')
    keywords = os.getenv('NEWSTOPICS').split(',')
    from_date = os.getenv('FROM')
    to_date = os.getenv('TO')
    language = os.getenv('LANGUAGE')
    fetch_news(api_keys, keywords, from_date, to_date, language)