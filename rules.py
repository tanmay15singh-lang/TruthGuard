from factcheck_api import check_fact

def evaluate_content(text):
    score = 0
    reasons = []

    text_lower = text.lower()

    # ---------- NEGATIVE SIGNALS ----------
    # Sensational language
    if any(word in text_lower for word in ["breaking", "shocking", "viral", "share this"]):
        score -= 2
        reasons.append("Sensational language detected")

    # Explicit lack of source
    if any(phrase in text_lower for phrase in ["no official source", "not confirmed"]):
        score -= 2
        reasons.append("No official confirmation mentioned")

    # Missing source entirely
    if "source:" not in text_lower:
        score -= 1
        reasons.append("No clear source provided")

    # ---------- POSITIVE SIGNALS ----------
    # Official / verified sources
    official_sources = [
    "official government",
    "government press",
    "ministry of",
    "official press release",
    "verified government",
    "source: official"
]

    if any(phrase in text_lower for phrase in official_sources):
     score += 2
     reasons.append("Official or verified source mentioned")

    # Fact-check similarity
    claims = check_fact(text)
    if claims:
        score += 1
        reasons.append("Similar claims found in fact-check sources")

    # ---------- FINAL DECISION ----------
    if score <= -2:
        credibility = "Low"
    elif -1 <= score <= 1:
        credibility = "Medium"
    else:
        credibility = "High"

    # ---------- FALLBACK ----------
    if not reasons:
        reasons.append("No major credibility issues detected")

    explanation = (
        "TruthGuard evaluates content using transparent rule-based analysis. "
        "It checks language tone, source credibility, and similarity to verified "
        "fact-check data to estimate trustworthiness."
    )

    return credibility, reasons, explanation
