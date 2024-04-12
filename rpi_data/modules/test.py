import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import lxml

url = "https://catalog.rpi.edu/content.php?filter%5B27%5D=CSCI&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=26&expand=&navoid=671&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter"

html = urlopen(url)
driver = webdriver.Firefox()
driver.get(url)

prereqs = dict()

links = driver.find_elements("xpath", "//a[@href]")
for link in links:
    if 'CSCI' in link.get_attribute("innerHTML"):
        s = link.get_attribute("innerHTML").replace('&nbsp;', ' ') 
        prereqs[s] = {}
        link.click()
    
soup = BeautifulSoup(driver.page_source, 'html.parser')    

tags = [tr.get_text() for tr in soup.select('td.block_content table.class_default tbody tr')]

print(len(tags))


        
driver.close()
        


        

