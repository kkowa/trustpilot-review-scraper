# # MONDAY.COM TABLE REQUIREMENT
# # FIRST NAME | LAST NAME | EMAIL | REVIEW DATE


import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from util import parse_date, output_data
import re

# Constants
COMPANY_NAME = "frontendsimplified.com"
MAX_PAGE_NUMBER = 11  # TODO: grab automatically as it will change
SORT_BY = "recency"

CARD_CLASS = "styles_reviewCardInner__UZk1x"
    
REVIEW_CUSTUMER_INFO_CLASS = "styles_consumerInfoWrapper__MOCv1"
CUSTUMER_NAME_CLASS = "typography_heading-xxs__UmE9o typography_appearance-default__t8iAq"
CUSTUMER_LOCATION_CLASS = "typography_body-m__k2UI7 typography_appearance-subtle__PYOVM styles_detailsIcon__ch_FY"

REVIEW_CONTENT_CLASS = "styles_reviewContentwrapper__W9Vqf"
REVIEW_DATE_CLASS = "typography_body-m__k2UI7 typography_appearance-default__t8iAq"
REVIEW_SCORE_CLASS = "star-rating_starRating__sdbkn star-rating_medium__Oj7C9"


reviews_list = []

output_folder = "data/processed"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through each page
for page_number in range(1, MAX_PAGE_NUMBER + 1):

    URL = f"https://www.trustpilot.com/review/{COMPANY_NAME}?page={page_number}&sort={SORT_BY}"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    review_cards = soup.find_all("div", class_=CARD_CLASS)
            
    for card in review_cards:
       
        # Customer Information
        custumer_info = card.find("aside", class_=REVIEW_CUSTUMER_INFO_CLASS)
        customer_name_tag = custumer_info.find("span", class_=CUSTUMER_NAME_CLASS)
        customer_name = customer_name_tag.text.strip() if customer_name_tag else "N/A"
        x = customer_name.split()
        
        if len(x) > 1:
            first_name = x[0] 
            last_name = " ".join(x[1:]) 
        else:
            first_name = x[0]
            last_name = ""  
        
        custumer_location_tag = custumer_info.find("div", class_=CUSTUMER_LOCATION_CLASS)
        custumer_location = custumer_location_tag.find("span").text.strip() if custumer_location_tag else "N/A"
        
        # Review Contents
        review_contents = card.find("section", class_=REVIEW_CONTENT_CLASS)
        
        review_score_tag = card.find("div", class_=REVIEW_SCORE_CLASS).find('img').get('alt')
        review_score = re.search(r'\d+', review_score_tag).group(0)
  
    
        review_submission_date_time_tag = review_contents.find("time")
        review_submission_date_time = parse_date(review_submission_date_time_tag.text.strip()) if review_submission_date_time_tag else "N/A"
        review_date, review_time = review_submission_date_time.split()


        reviews_list.append({
            "Name": first_name,
            "Last Name": last_name,
            "Review Date": review_date, 
            "Score": review_score
        })


reviews_df = pd.DataFrame(reviews_list)

output_data("data/processed", "reviews_data.xlsx", reviews_df)

print(f"Scraped {len(reviews_list)} reviews. Data saved to data/processed.")
