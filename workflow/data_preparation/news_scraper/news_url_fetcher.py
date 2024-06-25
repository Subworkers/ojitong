# 1) 뉴스 URL 가져오기
import requests
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup

def format_today_date(today_datetime: datetime):
    today = today_datetime.strftime('%Y.%m.%d')
    today_filter = today_datetime.strftime('%Y%m%d')
    return today, today_filter

def create_search_url(query: str, today: str, today_filter: str):
    return f"https://search.naver.com/search.naver?where=news&query={query}&sort=1&ds={today}&de={today}&nso=so:r,p:from{today_filter}to{today_filter}"

def fetch_html(url: str):
    response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch HTML")
        return None

def parse_news_urls(html: str, today: str):
    soup = BeautifulSoup(html, 'html.parser')
    news_urls = []
    for news_area in soup.find_all('div', class_='news_area'):
        title_element = news_area.find('a', class_='news_tit')
        date_element = news_area.find('span', class_='info')
        
        if title_element and date_element and (today in date_element.text or '시간 전' in date_element.text or '분 전' in date_element.text):
            news_urls.append(title_element['href'])
    return news_urls

def get_news_urls(query: str, today_datetime: datetime):
    today, today_filter = format_today_date(today_datetime)
    search_url = create_search_url(query, today, today_filter)
    html = fetch_html(search_url)
    
    if html:
        news_urls = parse_news_urls(html, today)
        return news_urls
    else:
        return []