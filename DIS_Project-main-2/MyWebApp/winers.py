import requests

api_key="chjka21r01qh5480hn3gchjka21r01qh5480hn40"

def get_news():
    news = requests.get(f"https://finnhub.io/api/v1/news?category=general&token={api_key}")
    news = news.json()
    return news

def print_news():
    news = get_news()
    for i in news:
        headline = i['headline']
        summary = i['summary']
        url = i['url']
    return headline, summary, url

