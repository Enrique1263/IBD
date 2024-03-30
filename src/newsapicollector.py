import os
from dotenv import load_dotenv
from newsapi import NewsApiClient

def fetch_news(api_keys, keywords, from_date, to_date, language):
    newsapi = NewsApiClient(api_key=api_keys[0])
    final_articles = {keyword: [] for keyword in keywords}
    for keyword in keywords:
        page = 1
        while True:
            try:
                response = newsapi.get_everything(q=keyword,
                                                from_param=from_date,
                                                to=to_date,
                                                language=language,
                                                page=page)
                if response['status'] == 'ok':
                    final_articles[keyword] += response['articles']
                    page += 1
            except Exception as e:
                e = dict(e.args[0])
                if e['code'] == 'rateLimited':
                    print('Rate limited, switching to next API key')
                    api_keys.append(api_keys.pop(0))
                    newsapi = NewsApiClient(api_key=api_keys[0])

                elif e['code'] == 'maximumResultsReached':
                    print('Maximum results reached, changing keyword')
                    break
                else:
                    print('Unknown error: ', e)
                    break
    
    return final_articles

if __name__ == '__main__':
    load_dotenv()
    api_keys = os.getenv('NEWSAPIKEY').split(',')
    keywords = os.getenv('NEWSTOPICS').split(',')
    from_date = os.getenv('FROM')
    to_date = os.getenv('TO')
    language = os.getenv('LANGUAGE')
    articles = fetch_news(api_keys, keywords, from_date, to_date, language)
    print(len(set([article['url'] for keyword in articles for article in articles[keyword]])))
    # print(articles)