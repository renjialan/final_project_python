import requests
import config  # Ensure this file contains your News API key
from datetime import datetime, timedelta

def fetch_news(keyword):
    base_url = 'https://newsapi.org/v2/everything?'
    date_a_month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    url = f'{base_url}q={keyword}&from={date_a_month_ago}&sortBy=publishedAt&apiKey={config.NEWS_API_KEY}'
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        print(f'Error fetching news for {keyword}: {response.status_code}')
        return []