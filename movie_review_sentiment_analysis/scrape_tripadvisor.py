import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


payload = { 'api_key': 'b5d04add6800e422b153f4a35019f736', 'url': 'https://www.tripadvisor.com/Attraction_Review-g308272-d10383031-Reviews-Shanghai_Disneyland-Shanghai.html', 'autoparse': 'true' }
response = requests.get('https://api.scraperapi.com/', params=payload)

if response.status_code==200:
    print("Page fectched successfully ")
    soup=BeautifulSoup(response.content,'html.parser')
    print(soup.prettify())
    # Extract reviews
    reviews = []
    review_cards = soup.find_all('div',{'data_automation':'reviewCard'})
    print(review_cards)

    for card in review_cards:
        try:
            review_text=card.find('div',class_='biGQs _P pZUbB KxBGd').find('span',class_='').text.strip()

            bubble_score = card.find('svg', class_='UctUV d H0').find('title').text.strip()

            reviews.append({'review':review_text,
                            'rating':bubble_score        })
            
        except AttributeError as e:
            print(f"Error extracting data from card: {e}")
            continue
    
    for i,review in enumerate(reviews,1):
        print(f"Review {i}: {reviews['review']}")
        print(f"Rating:{reviews['rating']}")
        print('_'*80)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

