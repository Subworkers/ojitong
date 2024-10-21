# 3) 결측 혹은 오류 데이터 보강
import re
from dateutil import parser
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

def fetch_article_text(driver, url):
    driver.get(url)
    elements_to_try = [
        (By.ID, 'pnlContent'),
        (By.TAG_NAME, 'article'),
        (By.CLASS_NAME, 'view_cont'),
        (By.CLASS_NAME, 'article_body'),
        (By.CLASS_NAME, 'article-body')
    ]

    fetched_text = ""
    for by, value in elements_to_try:
        try:
            fetched_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((by, value))
            ).text
            break  # If text is fetched successfully, break out of the loop
        except (NoSuchElementException, TimeoutException):
            continue  # Try the next element

    return fetched_text

def update_article_texts(df, driver):

    for index, row in df.iterrows():
        if pd.isna(row['text']) or len(row['text']) < 200:
            try:
                fetched_text = fetch_article_text(driver, row['url'])
                df.at[index, 'text'] = fetched_text
            except Exception as e:
                print(f"Error fetching article from {row['url']}: {e}")
    return df

def update_kbs_titles(df, driver):
    for index, row in df.iterrows():
        if row['title'] == 'KBS 뉴스':
            try:
                driver.get(row['url'])
                element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "h4.headline-title"))
                )
                real_title = element.text
                df.at[index, 'title'] = real_title  # 실제 제목으로 업데이트
            except (NoSuchElementException, TimeoutException, WebDriverException) as e:
                print(f"An error occurred for URL {row['url']}: {e}")
    return df

# publish_date의 null 값 처리
def fill_missing_publish_dates(df, driver):
    date_classes = ['news-date', 'date-repoter', 'article_info', 'article_byline', 'dates', 'dateFont', 'article_date']
    for index, row in df.iterrows():
        if pd.isna(row['publish_date']):
            url = row['url']
            try:
                driver.get(url)
            except TimeoutException:
                print(f"Timeout while loading {url}")
                continue
            
            publish_date = None
            for date_class in date_classes:
                date_elements = driver.find_elements(By.CLASS_NAME, date_class)
                for date_element in date_elements:
                    date_text = date_element.text
                    numbers = re.findall(r'\d+', date_text)
                    if len(numbers) >= 3:
                        publish_date = f"{numbers[0]}-{numbers[1].zfill(2)}-{numbers[2].zfill(2)}"
                        break
                if publish_date:
                    break
            
            if publish_date:
                try:
                    parsed_date = parser.parse(publish_date)
                    df.at[index, 'publish_date'] = parsed_date
                except ValueError as e:
                    print(f"Error parsing date from {url}: {e}")
    return df

