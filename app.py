from flask import Flask, request, jsonify, send_from_directory
from rules import evaluate_content
import os

app = Flask(__name__)

FRONTEND_DIR = os.path.join(os.getcwd(), "Frontend")

# Serve frontend
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

# Text analysis API
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    credibility, reasons, explanation = evaluate_content(text)

    return jsonify({
        "credibility": credibility,
        "reasons": reasons,
        "explanation": explanation
    })

if __name__ == "__main__":
    app.run(debug=True)