from transformers import pipeline

_offense_model = pipeline(
    "text-classification",
    model="martin-ha/toxic-comment-model",
    return_all_scores=True,
    truncation=True
)

def get_offense_score(text: str) -> float:
    try:
        preds = _offense_model(text)[0]
        offensive_labels = [p["score"] for p in preds if p["label"] not in ["non-toxic", "neutral"]]
        score = sum(offensive_labels) / len(offensive_labels)
        return round(score, 4)
    except Exception as e:
        print("Moderation model error:", e)
        return 0.0

