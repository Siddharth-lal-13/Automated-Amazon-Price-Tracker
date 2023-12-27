import requests
from bs4 import BeautifulSoup
import smtplib
import os

MY_EMAIL = os.environ["SMTPEMAIL"]
PASSWORD = os.environ["PASSWORD"]
TARGET_PRICE = 599

# Product Link
AMAZON_PRODUCT_URL = ("https://www.amazon.in/Blue-Aura-Multicolor-Assembly-Required/dp/B09GPQ755H/ref=sr_1_6?crid"
                      "=NUUAH0HC2LKC&keywords=naruto+action+figures&qid=1703595640&sprefix=naruto+%2Caps%2C300&sr=8-6")

# HTTP Header Details
HEADERS = {
    "User-Agent": os.environ["USERAGENT"],
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8,ja;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
}

response = requests.get(url=AMAZON_PRODUCT_URL, headers=HEADERS)
web_page_data = response.text

soup = BeautifulSoup(web_page_data, "html.parser")

price = soup.find(name="span", class_="a-offscreen").get_text()
price_only = float(price.split("₹")[1])

if price_only < TARGET_PRICE:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="siddharthlal99@gmail.com",    # the email where your alert emails will be forwarded.
            msg=f"Subject:Discount Appeared!!\n\nYour desired product price on Amazon is {price} which is below your "
                f"target price! It's the right time to buy!!".encode('utf-8')
        )
        