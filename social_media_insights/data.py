from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import numpy as np
import re
import os

import requests
from bs4 import BeautifulSoup 

def scrape_article_links(url):
    
    # Send a request to the Medium account
    response=requests.get(url)
    
    #Parse the HTML content of profile page
    soup=BeautifulSoup(response.content,'html.parser')
    
    article_links=[]
    article_blocks=soup.find_all('div',class_="bh l")
    for block in article_blocks:
        link=block.find('div',{'role':'link'}).get('data-href',None)
        
        if link:
            article_links.append(link)
            
    return list(set(article_links))

def scrape_articles_infinite_scroll(profile_url):
    # Set up the Selenium WebDriver (replace with the path to your WebDriver executable)
    driver = webdriver.Chrome()  # Adjust for your WebDriver
    driver.get(profile_url)
    time.sleep(3)  # Allow the page to load initially

    # Store all article links
    article_links = set()

    # Track scrolling
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for the new content to load

        # Find all article blocks dynamically
        article_blocks = driver.find_elements(By.CLASS_NAME, 'bh.l')  # Adjust class if necessary
        for block in article_blocks:
            # Find the 'data-href' attribute within each block
            try:
                link = block.find_element(By.CSS_SELECTOR, 'div[role="link"]').get_attribute('data-href')
                if link and link not in article_links:
                    article_links.add(link)
            except Exception as e:
                pass  # Skip if any block doesn't have the required structure

        # Check if the page has stopped loading more content
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Exit if no more content is being loaded
        last_height = new_height

    # Close the browser
    driver.quit()

    return list(article_links)



