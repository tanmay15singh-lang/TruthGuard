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


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "TruthGuard backend running",
        "frontend": "https://truth-guard-vert.vercel.app"
    })


# --------------------------------------------------
# TEXT CREDIBILITY API
# --------------------------------------------------
@app.route("/api/text", methods=["POST"])
def analyze_text():
    data = request.json
    content = data.get("content", "")
    use_llm = data.get("use_llm", False)

    if not content:
        return jsonify({"error": "No content provided"}), 400

    credibility, reasons, base_explanation = evaluate_content(content)

    if use_llm:
        explanation = (
            "This explanation is AI-assisted. The system analyzed language tone, "
            "source reliability indicators, and fact-check similarity signals "
            "to estimate credibility."
        )
    else:
        explanation = base_explanation

    return jsonify({
        "credibility": credibility,
        "reasons": reasons,
        "explanation": explanation
    })


# --------------------------------------------------
# IMAGE AI DETECTION API
# --------------------------------------------------
@app.route("/api/image", methods=["POST"])
def detect_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    try:
        level, confidence, signals = analyze_image(path)
    except Exception as e:
        return jsonify({
            "level": "Error",
            "confidence": 0,
            "signals": [str(e)]
        }), 500

    return jsonify({
        "media_type": "image",
        "ai_level": level,
        "confidence": confidence,
        "signals": signals
    })


# --------------------------------------------------
# VIDEO AI DETECTION API
# --------------------------------------------------
@app.route("/api/video", methods=["POST"])
def detect_video():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    try:
        level, confidence, signals = analyze_video(path)
    except Exception as e:
        return jsonify({
            "level": "Error",
            "confidence": 0,
            "signals": [str(e)]
        }), 500

    return jsonify({
        "media_type": "video",
        "ai_level": level,
        "confidence": confidence,
        "signals": signals
    })


# --------------------------------------------------
# RUN LOCAL
# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
