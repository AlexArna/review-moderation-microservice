from typing import Set, Dict, Any
from app.models import ReviewRequest  # Pydantic model used for review input

# Defining the custom list of banned words
BANNED_WORDS: Set[str] = {"badword1", "badword2", "scam", "fake"}

# Defining the criteria for spam detection (text length)
MIN_LENGTH: int = 5
MAX_LENGTH: int = 500

def is_spam(text: str) -> bool:
    """
    Detects simple spam patterns (text too short/long, specific words, etc).
    Returns True if the text is considered spam, False otherwise.
    """
    if len(text) < MIN_LENGTH or len(text) > MAX_LENGTH:
        return True
    lowered = text.lower()
    if 'buy now' in lowered or 'click here' in lowered:
        return True
    return False

def moderate_custom(review: ReviewRequest) -> Dict[str, Any]:
    """
    Moderation logic using a custom list of banned words and spam detection.
    Returns a dictionary with keys: decision, reason, user_id, business_id.
    """
    text = review.text.lower()
    for word in BANNED_WORDS:
        if word in text:
            return {
                "decision": "reject",
                "reason": f"contains banned word: {word}",
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
    # Accept all others for now
    return {
        "decision": "accept",
        "reason": "no banned words or spam detected",
        "user_id": review.user_id,
        "business_id": review.business_id
    }