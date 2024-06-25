# 3***REMOVED*** 결측 혹은 오류 데이터 보강

import pandas as pd
import numpy as np

def fetch_article_text(driver, url***REMOVED***:
    driver.get(url***REMOVED***
    elements_to_try = [
        (By.ID, 'pnlContent'***REMOVED***,
        (By.TAG_NAME, 'article'***REMOVED***,
        (By.CLASS_NAME, 'view_cont'***REMOVED***,
        (By.CLASS_NAME, 'article_body'***REMOVED***,
        (By.CLASS_NAME, 'article-body'***REMOVED***
    ***REMOVED***

    fetched_text = ""
    for by, value in elements_to_try:
        try:
            fetched_text = WebDriverWait(driver, 10***REMOVED***.until(
                EC.presence_of_element_located((by, value***REMOVED******REMOVED***
            ***REMOVED***.text
            break  # If text is fetched successfully, break out of the loop
        except (NoSuchElementException, TimeoutException***REMOVED***:
            continue  # Try the next element

    return fetched_text

def update_article_texts(df, driver***REMOVED***:

    for index, row in df.iterrows(***REMOVED***:
        if pd.isna(row['text'***REMOVED******REMOVED*** or len(row['text'***REMOVED******REMOVED*** < 200:
            try:
                fetched_text = fetch_article_text(driver, row['url'***REMOVED******REMOVED***
                df.at[index, 'text'***REMOVED*** = fetched_text
            except Exception as e:
                print(f"Error fetching article from {row['url'***REMOVED******REMOVED***: {e***REMOVED***"***REMOVED***
    return df

def update_kbs_titles(df, driver***REMOVED***:
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

    for index, row in df.iterrows(***REMOVED***:
        if row['title'***REMOVED*** == 'KBS 뉴스':
            try:
                driver.get(row['url'***REMOVED******REMOVED***
                element = WebDriverWait(driver, 10***REMOVED***.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "h4.headline-title"***REMOVED******REMOVED***
                ***REMOVED***
                real_title = element.text
                df.at[index, 'title'***REMOVED*** = real_title  # 실제 제목으로 업데이트
            except (NoSuchElementException, TimeoutException, WebDriverException***REMOVED*** as e:
                print(f"An error occurred for URL {row['url'***REMOVED******REMOVED***: {e***REMOVED***"***REMOVED***
    return df
