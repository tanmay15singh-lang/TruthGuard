from PIL import Image
import numpy as np
import cv2

def analyze_image(path):
    score = 0
    signals = []

    # --- 1. EXIF Metadata ---
    try:
        img = Image.open(path)
        exif = img._getexif()
        if exif is None:
            score += 2
            signals.append("Missing camera metadata (EXIF)")
    except:
        score += 2
        signals.append("Unable to read image metadata")

    # --- 2. Texture Smoothness ---
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    variance = np.var(image)
    if variance < 300:
        score += 1
        signals.append("Unnaturally smooth textures detected")

    # --- 3. Frequency Artifacts ---
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude = np.mean(np.abs(fshift))
    if magnitude > 1e6:
        score += 2
        signals.append("High-frequency artifacts detected")

    # --- Verdict ---
    if score >= 5:
        level = "High"
    elif score >= 3:
        level = "Medium"
    else:
        level = "Low"

    confidence = min(95, 40 + score * 12)

    return level, confidence, signals
