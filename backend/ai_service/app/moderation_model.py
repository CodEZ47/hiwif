from transformers import pipeline

_offense_model = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    truncation=True
)

def get_offense_score(text: str) -> float:
    try:
        result = _offense_model(text[:512])[0]
        score = float(result["score"])
        return round(score, 4)
    except Exception as e:
        print("Moderation model error:", e)
        return 0.0
