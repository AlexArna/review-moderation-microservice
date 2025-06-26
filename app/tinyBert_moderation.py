from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from app.models import ReviewRequest
from typing import Dict, Any

LABELS = ["clean", "profanity", "spam"]
LABEL_TO_DECISION = {
    0: ("accept", "no profanity or spam detected"),
    1: ("reject", "contains profanity (TinyBERT detected)"),
    2: ("flag", "flagged for suspected spam (TinyBERT detected)")
}

MODEL_PATH = "tinyBert_moderation_model_run2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

def moderate_tinybert(review: ReviewRequest) -> Dict[str, Any]:
    """ Moderate a review using TinyBERT.
        Return a dict compatible with ModerationResult.
    """
    # Preprocess: tokenize review text
    inputs = tokenizer(review.text, truncation=True, padding=True, max_length=128, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
        pred_idx = logits.argmax(-1).item()
    decision, reason = LABEL_TO_DECISION.get(pred_idx, ("flag", "unrecognized label"))
    return {
        "decision": decision,
        "reason": reason,
        "user_id": review.user_id,
        "business_id": review.business_id,
    }