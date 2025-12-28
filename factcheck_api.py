def check_fact(text):
    """
    Mock fact-check function.
    Returns True if text contains known trustworthy keywords.
    """
    trusted_keywords = ["who", "bbc", "reuters", "official", "study"]

    for word in trusted_keywords:
        if word in text.lower():
            return True

    return False
