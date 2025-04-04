import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from util import output_data
import re
import constants
from datetime import datetime

reviews_list = []

def rating_to_percentage(rating_text):
    # Extract all numbers from the text
    numbers = re.findall(r'\d+\.?\d*', rating_text)
    
    if len(numbers) >= 2:
        actual = float(numbers[0])
        maximum = float(numbers[1])
        percentage = (actual / maximum) * 100
        return f"{percentage:.0f}"
    else:
        return "Could not extract rating values"
    
def filter_reviews_by_name(reviews, name):
    pattern = re.compile(r'\b' + re.escape(name) + r'\b', re.IGNORECASE)
    filtered_reviews = []
    
    for review in reviews:
        title = review.get('Title', '')
        description = review.get('Description', '')
        
        # Add to filtered list ONLY if name appears in Title OR Description
        if pattern.search(title) or pattern.search(description):
            filtered_reviews.append(review)
    
    return filtered_reviews
 
for page_number in range(1, constants.MAX_PAGE_NUMBER + 1):

    URL = f"https://www.trustpilot.com/review/{constants.COMPANY_NAME}?page={page_number}&sort={constants.SORT_BY}"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    cards = soup.find_all("div", class_=constants.CARD)
    
    for card in cards: 

        # Custumer Information 
        custumer_name = card.find("span", class_=constants.NAME).text.strip() if card.find("span", class_=constants.NAME) else "N/A"
        custumer_location = card.find("span", class_=constants.LOCATION).text.strip() if card.find("span", class_=constants.LOCATION) else "N/A"
        
        # Review Info
        posting_datetime = card.find("div", class_=constants.POST_DATE).find("time").get('datetime').replace('Z', '+00:00')
        posting_datestamp = datetime.fromisoformat(posting_datetime).strftime("%B %d, %Y")
        
        # Review Content

        review_url="https://www.trustpilot.com" + str(card.find(class_=constants.REVIEW_CONTENT).find('a')['href'])
        score=rating_to_percentage(card.find("div", class_=constants.SCORE).find('img').get('alt')) 
        title=card.find("h2", class_=constants.TITLE).text.strip() if card.find("h2", class_=constants.TITLE) else "N/A"
        description=card.find("p", class_=constants.DESCRIPTION).text.strip() if card.find("p", class_=constants.DESCRIPTION) else "N/A"

        reviews_list.append({
            "Review URL": review_url,
            "Name": custumer_name,
            "Location": custumer_location,
            "Post Date": posting_datestamp,
            "Score": score,
            "Title": title,
            "Description": description
        })


all_reviews_df = pd.DataFrame(reviews_list)
kat_reviews_df = pd.DataFrame(filter_reviews_by_name(reviews_list, "Kat"))


output_data("data/processed", "all-reviews.xlsx", all_reviews_df)
output_data("data/processed", "kat-reviews.xlsx", kat_reviews_df) 


print(f"Scraped {len(reviews_list)} reviews. Data saved to data/processed.")
print(f"Kat has {len(kat_reviews_df)} reviews.")
