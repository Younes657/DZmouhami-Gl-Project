
import requests
from bs4 import BeautifulSoup
import re
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import abort
import models
from db import db
import time
def scrape_lawyers():

    base_url = "https://avocatalgerien.com/listings/page/{}/"
    #output_file = "lawyers.json"

    start_page = 59
    end_page = 62 #73

    data_list = []

    for page_number in range(start_page, end_page + 1):
        url = base_url.format(page_number)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all("article")

            for article in articles:
                lawyer_data = models.LawyerModel()

                lawyer_data.name = article.find("h2", class_="entry-title").text.strip()
                lawyer_data.Categories = article.find("p", class_="listing-cat").text.strip()
                lawyer_data.address = article.find("p", class_="listing-address").text.strip()
                lawyer_data.phoneNumber = article.find("p", class_="listing-phone").text.strip().replace("Tel:", "")
                email= article.find("li", id="listing-email")
                lawyer_data.email  = email.find("a").text.strip() if email else None
                rating_element = article.find("div", class_="stars-cont")
                lawyer_data.rating = int(rating_element.find("div", class_="stars")["class"][1][-1]) if rating_element else None
                #description = article.find("section", id="overview")
                #lawyer_data["Description"] = description.find("p").text.strip() if description else None
                
                data_list.append(lawyer_data)
            for obj in data_list:
                try:
                    db.session.add(obj)
                    db.session.commit()
                except SQLAlchemyError as e:
                    abort(500, message=str(e))
                time.sleep(1)

        else:
            print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")