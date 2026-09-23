import re


def normalize_text(text: str) -> str:
    """
    Convert text into a standard format for keyword matching.
    """

    text = text.lower()

    text = re.sub(r"[^\w\s]", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()