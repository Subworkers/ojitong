# 2***REMOVED*** 뉴스 기사 스크래핑
from newspaper import Article

def scrape_news_articles(news_urls***REMOVED***:
    articles_data = [***REMOVED***
    for url in news_urls:
        try:
            article = Article(url***REMOVED***
            article.download(***REMOVED***
            article.parse(***REMOVED***
            articles_data.append({
                'url': url,
                'title': article.title,
                'authors': article.authors,
                'publish_date': article.publish_date,
                'text': article.text
            ***REMOVED******REMOVED***
        except Exception as e:
            print(f"Failed to scrape article from {url***REMOVED***: {e***REMOVED***"***REMOVED***
    return articles_data
