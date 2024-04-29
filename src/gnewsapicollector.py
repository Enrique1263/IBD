import os
import pymongo
import requests
import json
import time
from datetime import datetime, timedelta

def fetch_news_gnews(api_keys, keywords, from_date, to_date, language):
    connection_string = os.getenv('CONNECTIONSTRING')
    client = pymongo.MongoClient(connection_string)
    db_name = 'newsDB'
    collection_name = 'gnews'
    col = client[db_name][collection_name]
    used_keys = []
    # Split date range into smaller segments (e.g., daily)
    start_date = datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.strptime(to_date, "%Y-%m-%d")
    delta = timedelta(days=1)  # Adjust as needed

    total_articles = []
    
    while start_date <= end_date:
        from_date_segment = start_date.strftime("%Y-%m-%d") + 'T00:00:00Z'
        to_date_segment = start_date.strftime("%Y-%m-%d") + 'T23:59:59Z'
        
        for keyword in keywords:  # Iterating over individual keywords
            if len(used_keys) == len(api_keys):
                print('All API keys used')
                break
            
            response = requests.get(f'https://gnews.io/api/v4/search?q={keyword}&from={from_date_segment}&to={to_date_segment}&lang={language}&token={api_keys[0]}')
            code = response.status_code
            response = json.loads(response.text)
            
            if code == 200:
                articles_to_insert =  response['articles']
                if len(articles_to_insert) == 0:
                    print(f'No articles found for {keyword} on {from_date_segment}')
                    continue
                else:
                    total_articles.extend(articles_to_insert)
                    col.insert_many(articles_to_insert)
                    print(f'Processed {keyword} for {from_date_segment}')
            elif code == 403:
                print('Rate limited, switching to next API key')
                api_keys.append(api_keys.pop(0))  # Rotate API keys
                used_keys.append(api_keys[-1])
            else:
                print('Unknown error: ', response)
                break
            
            time.sleep(1)  # Be respectful in your request pacing
        
        start_date += delta  # Move to the next segment

    file_name = f"./data/{collection_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    # Save the articles to a file, create a new file for each run
    with open(file_name, 'w') as file:
        for article in total_articles:
            file.write(json.dumps(article, default=str))
            file.write('\n')
    
    client.close()

if __name__ == '__main__':
    api_keys = os.getenv('GNEWSAPIKEY').split(',')
    keywords = os.getenv('GNEWSTOPICS').split(',')
    from_date = os.getenv('FROM')
    to_date = os.getenv('TO')
    language = os.getenv('LANGUAGE')
    fetch_news_gnews(api_keys, keywords, from_date, to_date, language)

