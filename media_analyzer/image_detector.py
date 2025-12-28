import cv2
import numpy as np

def analyze_image(path):
    img = cv2.imread(path)

    if img is None:
        return "Error", 0, ["Invalid image file"]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- Signal 1: Noise level ---
    noise = cv2.Laplacian(gray, cv2.CV_64F).var()

    # --- Signal 2: Edge density ---
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.mean(edges > 0)

    # --- Signal 3: Color variance ---
    color_var = np.mean(np.var(img, axis=(0, 1)))

    signals = []
    score = 0

    # Noise analysis
    if noise < 80:
        score += 1
        signals.append("Unnaturally low sensor noise (AI tendency)")
    else:
        signals.append("Natural sensor noise detected")

    # Edge analysis
    if edge_density < 0.03:
        score += 1
        signals.append("Over-smooth edges (AI tendency)")
    else:
        signals.append("Natural edge distribution")

    # Color analysis
    if color_var < 500:
        score += 1
        signals.append("Low color entropy (AI tendency)")
    else:
        signals.append("Natural color variation")

    # --- Final decision ---
    if score == 0:
        level = "Low"
        confidence = 15
    elif score == 1:
        level = "Medium"
        confidence = 40
    elif score == 2:
        level = "Medium"
        confidence = 60
    else:
        level = "High"
        confidence = 80

    return level, confidence, signals
