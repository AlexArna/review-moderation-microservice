from joblib import load
from app.models import ReviewRequest
from typing import Dict, Any

# Load model at import (pipeline includes preprocessing)
MODEL_PATH = "app/ml_moderation_model.joblib"
model = load(MODEL_PATH)

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
    pred_label = model.predict([review.text])[0]  # pipeline handles preprocessing
    decision, reason = LABEL_TO_DECISION.get(pred_label, ("flag", "unrecognized label"))
    return {
        "decision": decision,
        "reason": reason,
        "user_id": review.user_id,
        "business_id": review.business_id,
    }