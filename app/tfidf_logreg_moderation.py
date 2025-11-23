from joblib import load
from app.models import ReviewRequest
from typing import Dict, Any


MODEL_PATH = "app/ml_moderation_model.joblib"
try:
    model = load(MODEL_PATH)
# Handle error at startup
except Exception:
    model = None

LABEL_TO_DECISION = {
    "clean": ("accept", "no profanity or spam detected"),
    "profanity": ("reject", "contains profanity (ML detected)"),
    "spam": ("flag", "flagged for suspected spam (ML detected)")
}

def moderate_tfidf_logreg(review: ReviewRequest) -> Dict[str, Any]:
    """
    Moderates a review using the trained TF-IDF + Logistic Regression pipeline.
    Returns a dict compatible with ModerationResult.
    """
    try:
        if model is None:
            raise RuntimeError("Model failed to load at startup")
        prediction = model.predict([review.text]) # expected to be a list
        if not prediction: # list is empty
            decision, reason = ("flag", "empty label")
        else:
            pred_label = prediction[0]
            decision, reason = LABEL_TO_DECISION.get(pred_label, ("flag", "unrecognized label"))
    except Exception:
        decision, reason = ("flag", "model exception")
    return {
        "decision": decision,
        "reason": reason,
        "user_id": review.user_id,
        "business_id": review.business_id,
        }