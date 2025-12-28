import cv2
from .image_detector import analyze_image
import tempfile
import os

def analyze_video(path):
    cap = cv2.VideoCapture(path)
    frame_count = 0
    scores = []
    signals = set()

    while cap.isOpened() and frame_count < 5:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        temp_path = tempfile.mktemp(suffix=".jpg")
        cv2.imwrite(temp_path, frame)

        level, confidence, frame_signals = analyze_image(temp_path)
        scores.append(confidence)
        signals.update(frame_signals)

        os.remove(temp_path)

    cap.release()

    avg_conf = int(sum(scores) / len(scores)) if scores else 50

    if avg_conf >= 75:
        level = "High"
    elif avg_conf >= 55:
        level = "Medium"
    else:
        level = "Low"

    return level, avg_conf, list(signals)
