import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os

URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
headers = {
    "User-Agent": os.environ["USER_AGENT"],
    "Accept-Language": "en-US,en;q=0.5",
}

my_email = os.environ["MY_EMAIL"]
password = os.environ["PASSWORD"]


response = requests.get(URL, headers=headers)
site_html = response.text

soup = BeautifulSoup(site_html, "lxml")

item_price = soup.find(name="span", class_="a-offscreen").getText()
price_without_currency = item_price.split("$")[1]
price_float = float(price_without_currency)

item_title = soup.find(name="span", id="productTitle").getText().strip()
BUY_PRICE = 100

if price_float < BUY_PRICE:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=my_email,
                            msg=f"Subject: Amazon Price Alert!\n\n{item_title} is now {item_price}!"
                                f"\nBuy it at {URL}".encode("utf-8")
                            )