import os
from newsapi import NewsApiClient
import json
from datetime import datetime

def fetch_news(api_keys, keywords, from_date, to_date, language):

    total_articles = []

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
                    if len(articles_to_insert) == 0:
                        print('No articles found')
                    else:
                        total_articles.extend(articles_to_insert)
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

    file_name = f"/app/data/newsapi/newsapi_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    with open(file_name, 'w') as file:
        for article in total_articles:
            json.dump(article, file, default=str)
            file.write('\n')
        


    

if __name__ == '__main__':
    api_keys = os.getenv('NEWSAPIKEY').split(',')
    keywords = os.getenv('NEWSTOPICS').split(',')
    from_date = os.getenv('FROM')
    to_date = os.getenv('TO')
    language = os.getenv('LANGUAGE')
    fetch_news(api_keys, keywords, from_date, to_date, language)