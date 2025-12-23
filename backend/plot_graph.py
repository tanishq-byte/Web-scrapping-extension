import json
import os
import requests

# ==============================
# CONFIG
# ==============================

GEMINI_API_KEY = os.getenv("AIzaSyCrLsb-q8YnpVWsn9h8f7Piklgh7V-oxEk")  # safer than hardcoding
MODEL = "gemini-2.5-flash"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

CROP_DATA_PATH = os.path.join(OUTPUT_DIR, "crop_data.json")
REPORT_PATH = os.path.join(OUTPUT_DIR, "farmer_report.txt")

GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent?key={GEMINI_API_KEY}"
)

# ==============================
# VALIDATIONS
# ==============================

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not set in environment")

if not os.path.exists(CROP_DATA_PATH):
    raise FileNotFoundError("❌ crop_data.json not found")

# ==============================
# LOAD DATA
# ==============================

with open(CROP_DATA_PATH, "r", encoding="utf-8") as f:
    crop_data = json.load(f)

# ==============================
# PROMPT
# ==============================

prompt = f"""
You are an agricultural market analyst.

Given the following market price data (JSON),
generate a farmer-friendly report with:

1. Overall price trend
2. Best zones to sell
3. Lowest price zones (avoid selling there)
4. Simple advice for farmers
5. No technical jargon

Return PLAIN TEXT only.

DATA:
{json.dumps(crop_data, indent=2)}
"""

# ==============================
# GEMINI REQUEST
# ==============================

headers = {"Content-Type": "application/json"}

payload = {
    "contents": [
        {
            "parts": [{"text": prompt}]
        }
    ]
}

print("🤖 Sending data to Gemini...")

response = requests.post(
    GEMINI_URL,
    headers=headers,
    json=payload,
    timeout=60
)

if response.status_code != 200:
    raise RuntimeError(
        f"❌ Gemini API error {response.status_code}: {response.text}"
    )

result = response.json()

try:
    report_text = result["candidates"][0]["content"]["parts"][0]["text"]
except Exception:
    raise RuntimeError("❌ Unexpected Gemini response format")

# ==============================
# SAVE REPORT
# ==============================

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report_text)

print("✅ Farmer report generated successfully")
