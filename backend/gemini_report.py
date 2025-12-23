import json
import requests
import os

# ==============================
# GEMINI CONFIG (HARDCODED)
# ==============================
GEMINI_API_KEY = "AIzaSyCrLsb-q8YnpVWsn9h8f7Piklgh7V-oxEk"
MODEL = "gemini-2.5-flash"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

INPUT_JSON = os.path.join(OUTPUT_DIR, "crop_data.json")
REPORT_FILE = os.path.join(OUTPUT_DIR, "farmer_report.txt")

GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent?key={GEMINI_API_KEY}"
)

# ==============================
# LOAD DATA
# ==============================
if not os.path.exists(INPUT_JSON):
    raise RuntimeError("crop_data.json not found")

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

prompt = f"""
You are an agricultural market expert.

Generate a farmer-friendly market report with:
- Average price
- Best selling centre and zone
- Lowest price centre and zone
- Clear selling advice

DATA:
{json.dumps(data["data"], indent=2)}
"""

payload = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ]
}

headers = {
    "Content-Type": "application/json"
}

# ==============================
# CALL GEMINI
# ==============================
response = requests.post(
    GEMINI_URL,
    headers=headers,
    json=payload,
    timeout=60
)

if response.status_code != 200:
    raise RuntimeError(
        f"Gemini API error {response.status_code}: {response.text}"
    )

result = response.json()
report_text = result["candidates"][0]["content"]["parts"][0]["text"]

# ==============================
# SAVE REPORT
# ==============================
with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(report_text)

print("✅ Gemini report generated successfully")
