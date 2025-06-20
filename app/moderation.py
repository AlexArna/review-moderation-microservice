BANNED_WORDS = {"badword1", "badword2", "scam", "fake"}
MIN_LENGTH = 10

def moderate_review(review):
    text = review.text.lower()
    for word in BANNED_WORDS:
        if word in text:
            return {
                "decision": "reject",
                "reason": f"Contains banned word: {word}",
                "user_id": review.user_id,
                "business_id": review.business_id
            }
    if len(text) < MIN_LENGTH:
        return {
            "decision": "flag",
            "reason": "Review too short",
            "user_id": review.user_id,
            "business_id": review.business_id
        }
    # Accept all others for now
    return {
        "decision": "accept",
        "reason": "Clean review",
        "user_id": review.user_id,
        "business_id": review.business_id
    }