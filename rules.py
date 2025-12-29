from factcheck_api import check_fact

def evaluate_content(text: str):
    reasons = []
    text_lower = text.lower()

    # ---------- HARD LOW DETECTION (ABSOLUTE) ----------

    sensational_words = [
        "breaking", "shocking", "viral",
        "share this", "share fast", "urgent"
    ]

    denial_phrases = [
        "no official source",
        "not confirmed",
        "unverified",
        "rumor"
    ]

    sensational = any(w in text_lower for w in sensational_words)
    no_confirmation = any(p in text_lower for p in denial_phrases)
    has_source = "source:" in text_lower

    # 🚨 ABSOLUTE RULES — NO RECOVERY
    if sensational:
        reasons.append("Sensational language detected")

    if no_confirmation:
        reasons.append("No official confirmation mentioned")

    if sensational and (no_confirmation or not has_source):
        return "Low", reasons, explanation("Low")

    # ---------- SCORING (ONLY CLEAN CONTENT REACHES HERE) ----------

    score = 0

    if not has_source:
        score -= 2
        reasons.append("No clear source provided")

    official_sources = [
        "official government",
        "government press",
        "ministry of",
        "official press release",
        "verified government",
        "source: official",
        "source: government"
    ]

    has_official_source = any(p in text_lower for p in official_sources)

    if has_official_source:
        score += 3
        reasons.append("Official or verified source mentioned")

    # ⚠️ Fact-check ONLY applies if no sensational flags
    claims = check_fact(text)
    if claims and not sensational:
        score += 1
        reasons.append("Similar claims found in fact-check sources")

    # ---------- FINAL DECISION ----------

    if score >= 3:
        credibility = "High"
    elif score >= 0:
        credibility = "Medium"
    else:
        credibility = "Low"

    return credibility, reasons, explanation(credibility)


def explanation(level):
    return (
        f"TruthGuard assigns '{level}' credibility using strict rule-based checks. "
        f"Content flagged as sensational or unverified cannot receive high credibility."
    )