import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv


load_dotenv()

url = os.getenv("PRODUCT_URL")
print(url)
sender = os.getenv("SENDER_EMAIL")
to_email = os.getenv("TO_EMAIL")
smtp_user = os.getenv("SMTP_USER")
smtp_pass = os.getenv("SMTP_PASS")

def check_stock():
    print("In stock checker method")
    session = requests.Session()
    session.cookies.set("pincode", "500081")
    r = session.get(url, timeout=400)
    print(r)
    soup = BeautifulSoup(r.text, "html.parser")
    print(soup.prettify())  # check if "Add to Cart" is present now
    # Adjust the condition below to detect stock on Amul website
    if "Add to Cart" in r.text:
        return True
    return False

def send_email():
    msg = MIMEText(f"Product is now in stock: {url}")
    msg["Subject"] = "Stock Alert!"
    msg["From"] = sender
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

if check_stock():
    send_email()
    print("Stock available, email sent.")
else:
    print("Not in stock.")

print("Finally kuch toh hua")
