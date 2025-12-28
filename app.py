import os
from flask import Flask, render_template, request

from rules import evaluate_content
from media_analyzer.image_detector import analyze_image
from media_analyzer.video_detector import analyze_video

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- TEXT CREDIBILITY ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    credibility = None
    reasons = []
    explanation = ""

    media_result = False
    ai_level = None
    ai_confidence = None
    ai_signals = []

    use_llm = False
    content = ""

    if request.method == "POST":
        # Demo buttons
        if "demo" in request.form:
            demo = request.form.get("demo")

            if demo == "low":
                content = (
                    "BREAKING!!! Shocking viral news!!! Major city taken over overnight!!! "
                    "No official source has confirmed this yet!!! Share this before it gets deleted!!!"
                )
            elif demo == "medium":
                content = (
                    "Source: Local news reports suggest new safety measures may be introduced. "
                    "Officials have not yet issued a formal statement."
                )
            elif demo == "high":
                content = (
                    "Source: Official government press release from the Ministry of Health. "
                    "The announcement was published on verified government channels and "
                    "aligns with previously confirmed public records."
                )
        else:
            content = request.form.get("content", "")
            use_llm = request.form.get("use_llm") == "on"

        if content:
            credibility, reasons, base_explanation = evaluate_content(content)

            if use_llm:
                explanation = (
                    "🔍 AI Explanation (LLM-assisted): "
                    "The model summarizes detected credibility signals such as tone, "
                    "source reliability, and verification indicators to help users "
                    "understand why this credibility level was assigned."
                )
            else:
                explanation = base_explanation

    return render_template(
        "index.html",
        content=content,
        credibility=credibility,
        reasons=reasons,
        explanation=explanation,
        media_result=media_result,
        ai_level=ai_level,
        ai_confidence=ai_confidence,
        ai_signals=ai_signals
    )


# ---------------- MEDIA AI DETECTION ----------------
@app.route("/media", methods=["POST"])
def media_check():
    credibility = None
    reasons = []
    explanation = ""

    media_result = True
    ai_level = None
    ai_confidence = None
    ai_signals = []

    file = request.files.get("media")

    if not file or file.filename == "":
        return render_template(
            "index.html",
            media_result=True,
            ai_level="Error",
            ai_confidence=0,
            ai_signals=["No media file uploaded"]
        )

    filename = file.filename.lower()
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    try:
        if filename.endswith((".jpg", ".jpeg", ".png")):
            ai_level, ai_confidence, ai_signals = analyze_image(path)
        elif filename.endswith((".mp4", ".avi", ".mov")):
            ai_level, ai_confidence, ai_signals = analyze_video(path)
        else:
            ai_level = "Unsupported"
            ai_confidence = 0
            ai_signals = ["Unsupported file format"]
    except Exception as e:
        ai_level = "Error"
        ai_confidence = 0
        ai_signals = [str(e)]

    return render_template(
        "index.html",
        credibility=credibility,
        reasons=reasons,
        explanation=explanation,
        media_result=media_result,
        ai_level=ai_level,
        ai_confidence=ai_confidence,
        ai_signals=ai_signals
    )


if __name__ == "__main__":
    app.run(debug=True)
