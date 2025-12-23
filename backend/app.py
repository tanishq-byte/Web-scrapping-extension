from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import zipfile
from io import BytesIO

app = Flask(__name__)
CORS(app)

# ==============================
# PATH CONFIG
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

RAW_HTML_FILE = os.path.join(OUTPUT_DIR, "raw_html.txt")
REPORT_FILE = os.path.join(OUTPUT_DIR, "farmer_report.txt")
GRAPH_FILE = os.path.join(OUTPUT_DIR, "price_by_zone.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# TEST ROUTE
# ==============================
@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "status": "ok",
        "message": "Backend is running"
    })

# ==============================
# SCRAPE ROUTE (RAW HTML)
# ==============================
@app.route("/scrape", methods=["POST"])
def scrape():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({
                "status": "error",
                "message": "URL not provided"
            }), 400

        subprocess.run(
            ["python3", "scrap.py", url],
            cwd=BASE_DIR,
            check=True
        )

        if not os.path.exists(RAW_HTML_FILE):
            return jsonify({
                "status": "error",
                "message": "raw_html.txt not generated"
            }), 500

        with open(RAW_HTML_FILE, "r", encoding="utf-8") as f:
            raw_html = f.read()

        return jsonify({
            "status": "success",
            "raw_output": raw_html
        })

    except subprocess.CalledProcessError:
        return jsonify({
            "status": "error",
            "message": "Scraping process failed"
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ==============================
# REPORT ROUTE (CALLS GEMINI)
# ==============================
@app.route("/report", methods=["GET"])
def report():
    try:
        # Call Gemini report generator
        subprocess.run(
            ["python3", "gemini_report.py"],
            cwd=BASE_DIR,
            check=True
        )

        if not os.path.exists(REPORT_FILE):
            return jsonify({
                "status": "error",
                "message": "Report file not created"
            }), 500

        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            report_text = f.read()

        return jsonify({
            "status": "success",
            "report": report_text
        })

    except subprocess.CalledProcessError:
        return jsonify({
            "status": "error",
            "message": "Gemini API failed or quota exceeded"
        }), 500

# ==============================
# GRAPH ROUTE (IMAGE)
# ==============================
@app.route("/graph", methods=["GET"])
def graph():
    if not os.path.exists(GRAPH_FILE):
        return jsonify({
            "status": "error",
            "message": "Graph image not found"
        }), 404

    return send_file(GRAPH_FILE, mimetype="image/png")

# ==============================
# DOWNLOAD ZIP (REPORT + IMAGE)
# ==============================
@app.route("/download", methods=["GET"])
def download():
    try:
        if not os.path.exists(REPORT_FILE):
            return jsonify({
                "status": "error",
                "message": "Report not generated yet"
            }), 400

        memory_file = BytesIO()

        with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(REPORT_FILE, arcname="farmer_report.txt")
            if os.path.exists(GRAPH_FILE):
                zipf.write(GRAPH_FILE, arcname="price_by_zone.png")

        memory_file.seek(0)

        return send_file(
            memory_file,
            as_attachment=True,
            download_name="crop_market_report.zip"
        )

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ==============================
# START SERVER
# ==============================
if __name__ == "__main__":
    print("🚀 Backend server started successfully")
    print("🌐 Listening on http://localhost:8000")
    app.run(port=8000, debug=True)
