from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def initialize_webdriver(***REMOVED***:
    chrome_options = Options(***REMOVED***
    chrome_options.add_argument('--headless'***REMOVED***
    chrome_options.add_argument('--no-sandbox'***REMOVED***
    chrome_options.add_argument('--disable-dev-shm-usage'***REMOVED***
    chrome_options.add_argument('--disable-gpu'***REMOVED***
    chrome_options.add_argument('--remote-debugging-port=9222'***REMOVED***  # This can help avoid some common errors
    service = Service(ChromeDriverManager(***REMOVED***.install(***REMOVED******REMOVED***
    driver = webdriver.Chrome(service=service, options=chrome_options***REMOVED***
    return driver
