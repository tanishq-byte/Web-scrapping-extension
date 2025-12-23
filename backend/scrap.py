import sys
import requests
from bs4 import BeautifulSoup
import os
import json

# ==============================
# INPUT VALIDATION
# ==============================
if len(sys.argv) < 2:
    raise RuntimeError("❌ No URL provided")

url = sys.argv[1]

headers = {
    "User-Agent": "Mozilla/5.0"
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

RAW_HTML_FILE = os.path.join(OUTPUT_DIR, "raw_html.txt")
RAW_TEXT_FILE = os.path.join(OUTPUT_DIR, "raw_text.txt")

# ==============================
# FETCH WEBSITE
# ==============================
response = requests.get(url, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

# ==============================
# SAVE RAW HTML
# ==============================
with open(RAW_HTML_FILE, "w", encoding="utf-8") as f:
    f.write(soup.prettify())

# ==============================
# SAVE CLEAN TEXT (BS4 OUTPUT)
# ==============================
clean_text = soup.get_text(separator="\n", strip=True)

with open(RAW_TEXT_FILE, "w", encoding="utf-8") as f:
    f.write(clean_text)

print("✅ Raw HTML and BeautifulSoup text extracted")
