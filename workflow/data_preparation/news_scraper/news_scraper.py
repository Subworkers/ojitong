# 2) 뉴스 기사 스크래핑
from newspaper import Article

def scrape_news_articles(news_urls):
    articles_data = []
    for url in news_urls:
        try:
            article = Article(url)
            article.download()
            article.parse()
            articles_data.append({
                'url': url,
                'title': article.title,
                'authors': article.authors,
                'publish_date': article.publish_date,
                'text': article.text
            })
        except Exception as e:
            print(f"Failed to scrape article from {url}: {e}")
    return articles_data
