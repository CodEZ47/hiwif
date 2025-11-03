import re
import unicodedata

def sanitize_text(text: str, max_length: int = 2000) -> str:
    """Remove prompt-injection patterns, normalize unicode, and truncate."""
    # Normalize Unicode (e.g., homoglyph attacks)
    text = unicodedata.normalize("NFKC", text)
    # Remove code-like or instruction-like patterns
    text = re.sub(
        r"(ignore|system|instruction|prompt|token|password|api key|sudo|execute|command)",
        "",
        text,
        flags=re.IGNORECASE,
    )
    # Strip special dangerous symbols
    text = re.sub(r"[{}<>$`]", "", text)
    # Truncate
    return text[:max_length].strip()


def compute_section_weight(post_data: dict) -> float:
    weights = {
        "title": 0.05,
        "contextDescription": 0.10,
        "intendedGoal": 0.10,
        "whatHappened": 0.15,
        "whyItFailed": 0.20,
        "lessonLearned": 0.25,
        "adviceToOthers": 0.15,
    }
    filled = [k for k, v in post_data.items() if v and k in weights]
    completeness = sum(weights[k] for k in filled)
    return round(completeness, 2)
