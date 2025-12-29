from factcheck_api import check_fact

def evaluate_content(text: str):
    score = 0
    reasons = []

    text_lower = text.lower()

    # ================= NEGATIVE SIGNALS =================

    # Sensational language (strong negative)
    if any(word in text_lower for word in [
        "breaking", "shocking", "viral", "share this", "share fast", "urgent"
    ]):
        score -= 3
        reasons.append("Sensational language detected")

    # Explicit lack of confirmation (strong negative)
    if any(phrase in text_lower for phrase in [
        "no official source",
        "not confirmed",
        "unverified",
        "rumor"
    ]):
        score -= 3
        reasons.append("No official confirmation mentioned")

    # Missing source entirely
    if "source:" not in text_lower:
        score -= 2
        reasons.append("No clear source provided")

    # ================= POSITIVE SIGNALS =================

    official_sources = [
        "official government",
        "government press",
        "ministry of",
        "official press release",
        "verified government",
        "source: official",
        "source: government"
    ]

    has_official_source = any(
        phrase in text_lower for phrase in official_sources
    )

    if has_official_source:
        score += 3
        reasons.append("Official or verified source mentioned")

    # Fact-check similarity (weak positive)
    claims = check_fact(text)
    if claims:
        score += 1
        reasons.append("Similar claims found in fact-check sources")

    # ================= HARD SAFETY GUARDS =================
    # These prevent LOW from ever becoming HIGH

    # If sensational + no official source → ALWAYS LOW
    if (
        any(word in text_lower for word in ["breaking", "shocking", "viral"])
        and not has_official_source
    ):
        credibility = "Low"
        return credibility, reasons, base_explanation(credibility)

    # ================= FINAL DECISION =================

    if score <= -3:
        credibility = "Low"
    elif -2 <= score <= 2:
        credibility = "Medium"
    else:
        credibility = "High"

    return credibility, reasons, base_explanation(credibility)


def base_explanation(level: str):
    return (
        f"TruthGuard evaluated this content using transparent rule-based analysis. "
        f"The credibility level '{level}' was assigned based on language tone, "
        f"source reliability, and verification signals."
    )