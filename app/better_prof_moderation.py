# using  rule-based profanity filter
from better_profanity import profanity
from app.custom_moderation import is_spam
from app.models import ReviewRequest  # Pydantic model used for review input
from typing import Dict, Any

profanity.load_censor_words()

def moderate_better_prof(review: ReviewRequest) -> Dict[str, Any]:
    """
    Moderation logic using better_profanity as a rule-based profanity filter.
    Returns: dict with keys: decision, reason, user_id, business_id
    """
    text = review.text.lower()
    if profanity.contains_profanity(text):
        return {
            "decision": "reject",
            "reason": "contains profanity (better_profanity wordlist)",
            "user_id": review.user_id,
            "business_id": review.business_id
        }
    if is_spam(text):
        return {
            "decision": "flag",
            "reason": "flagged for suspected spam",
            "user_id": review.user_id,
            "business_id": review.business_id
        }
    return {
        "decision": "accept",
        "reason": "no profanity or spam detected",
        "user_id": review.user_id,
        "business_id": review.business_id
    }
