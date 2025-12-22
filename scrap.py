import requests
from bs4 import BeautifulSoup

url = "http://127.0.0.1:5500/index.html"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

with open("scrapHTML.txt", "w", encoding="utf-8") as file:
    file.write(soup.prettify())

print("✅ HTML saved to scrapHTML.txt")
