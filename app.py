import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from rules import evaluate_content
from media_analyzer.image_detector import analyze_image
from media_analyzer.video_detector import analyze_video

app = Flask(__name__)
CORS(app)  # VERY IMPORTANT for Vercel frontend

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- HEALTH CHECK ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "TruthGuard backend running",
        "frontend": "https://truth-guard-vert.vercel.app"
    })


# ---------------- TEXT CREDIBILITY API ----------------
@app.route("/analyze-text", methods=["POST"])
def analyze_text():
    data = request.json
    content = data.get("content", "")
    use_llm = data.get("use_llm", False)

    if not content:
        return jsonify({"error": "No content provided"}), 400

    credibility, reasons, base_explanation = evaluate_content(content)

    explanation = base_explanation
    if use_llm:
        explanation = (
            "AI-assisted explanation: The system evaluated tone, "
            "source indicators, and verification signals to estimate credibility."
        )

    return jsonify({
        "credibility": credibility,
        "reasons": reasons,
        "explanation": explanation
    })


# ---------------- MEDIA AI DETECTION API ----------------
@app.route("/media", methods=["POST"])
def media_check():
    file = request.files.get("media")

    if not file or file.filename == "":
        return jsonify({
            "ai_level": "Error",
            "confidence": 0,
            "signals": ["No media file uploaded"]
        }), 400

    filename = file.filename.lower()
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    try:
        if filename.endswith((".jpg", ".jpeg", ".png")):
            ai_level, confidence, signals = analyze_image(path)
        elif filename.endswith((".mp4", ".avi", ".mov")):
            ai_level, confidence, signals = analyze_video(path)
        else:
            ai_level = "Unsupported"
            confidence = 0
            signals = ["Unsupported file format"]
    except Exception as e:
        ai_level = "Error"
        confidence = 0
        signals = [str(e)]

    return jsonify({
        "ai_level": ai_level,
        "confidence": confidence,
        "signals": signals
    })


if __name__ == "__main__":
    app.run(debug=True)
