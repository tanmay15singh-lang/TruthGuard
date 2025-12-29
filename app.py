from flask import Flask, render_template, request, jsonify
from rules import evaluate_content

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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