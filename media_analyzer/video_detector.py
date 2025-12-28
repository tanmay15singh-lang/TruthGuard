import cv2
import numpy as np

def analyze_video(path):
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        return "Error", 0, ["Invalid video file"]

    frame_count = 0
    smooth_frames = 0
    signals = []

    while frame_count < 15:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        noise = cv2.Laplacian(gray, cv2.CV_64F).var()

        if noise < 60:
            smooth_frames += 1

        frame_count += 1

    cap.release()

    if frame_count == 0:
        return "Error", 0, ["No frames detected"]

    smooth_ratio = smooth_frames / frame_count

    if smooth_ratio < 0.3:
        level = "Low"
        confidence = 20
        signals.append("Natural temporal noise detected")
    elif smooth_ratio < 0.6:
        level = "Medium"
        confidence = 50
        signals.append("Partial AI-like smoothing across frames")
    else:
        level = "High"
        confidence = 75
        signals.append("Consistent AI-style frame smoothing")

    return level, confidence, signals
