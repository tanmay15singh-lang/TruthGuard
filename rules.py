from factcheck_api import check_fact

def evaluate_content(text: str):
    reasons = []
    text_lower = text.lower()

    # ---------- HARD FAIL CONDITIONS (NO RECOVERY) ----------

    sensational = any(word in text_lower for word in [
        "breaking", "shocking", "viral", "share fast", "share this", "urgent"
    ])

    no_confirmation = any(phrase in text_lower for phrase in [
        "no official source",
        "not confirmed",
        "unverified",
        "rumor"
    ])

    has_source = "source:" in text_lower

    # 🚨 RULE 1: Sensational + no confirmation = ALWAYS LOW
    if sensational and no_confirmation:
        reasons.append("Sensational language detected")
        reasons.append("No official confirmation mentioned")
        return "Low", reasons, explanation("Low")

    # 🚨 RULE 2: Sensational + no source = ALWAYS LOW
    if sensational and not has_source:
        reasons.append("Sensational language detected")
        reasons.append("No clear source provided")
        return "Low", reasons, explanation("Low")

    # ---------- SCORING (ONLY IF NOT HARD-FAILED) ----------

    score = 0

    if sensational:
        score -= 2
        reasons.append("Sensational language detected")

    if no_confirmation:
        score -= 2
        reasons.append("No official confirmation mentioned")

    if not has_source:
        score -= 1
        reasons.append("No clear source provided")

    # ---------- POSITIVE SIGNALS ----------

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

    claims = check_fact(text)
    if claims:
        score += 1
        reasons.append("Similar claims found in fact-check sources")

    # ---------- FINAL DECISION ----------

    if score <= -2:
        credibility = "Low"
    elif -1 <= score <= 2:
        credibility = "Medium"
    else:
        credibility = "High"

    return credibility, reasons, explanation(credibility)


def explanation(level):
    return (
        f"TruthGuard assigns '{level}' credibility using transparent rules. "
        f"The decision is based on language tone, source reliability, "
        f"and verification signals."
    )