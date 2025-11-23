import pytest
from pydantic import ValidationError
from app.custom_moderation import is_spam, moderate_custom
from app.better_prof_moderation import moderate_better_prof
from app.models import ReviewRequest, ModerationResult, ModerationDecision

@pytest.mark.parametrize("text, expected", [
    # Length edge cases
    ("Ok", True),
    ("", True),
    ("The service was excellent and the meal was delicious." * 10, True),
    ("The service was excellent and the meal was delicious.", False),
    # Spam phrase detection
    ("Buy now this amazing opportunity!", True),
    ("Click here to get rich quick!", True),
    ("BUY NOW", True),
    ("click HERE", True)
], ids=["too_short", "empty", "too_long", "clean", "promotion", "clickbait", "promo_upper",
        "click_upper"])
def test_is_spam_cases(text, expected):
    assert is_spam(text) == expected

def test_review_request_creation_valid():
    review = ReviewRequest(user_id="usr1", business_id="bus1", text="Amazing food!")
    assert review.user_id == "usr1"
    assert review.business_id == "bus1"
    assert review.text == "Amazing food!"

def test_review_request_missing_field():
    with pytest.raises(ValidationError):
        ReviewRequest(user_id="usr1", business_id="bus1")

def test_review_request_incorrect_type():
    with pytest.raises(ValidationError):
        ReviewRequest(user_id="usr1", business_id="bus1", text=1)

def test_moderation_result_valid_string():
    result = ModerationResult(decision="accept", reason="legit review", user_id="usr1", business_id="bus1")
    assert result.decision == "accept"
    assert result.reason == "legit review"
    assert result.user_id == "usr1"
    assert result.business_id == "bus1"

def test_moderation_result_valid_enum():
    result = ModerationResult(decision=ModerationDecision.flag, reason="spam", user_id="usr1", business_id="bus1")
    assert result.decision == ModerationDecision.flag

def test_moderation_result_incorrect_decision():
    with pytest.raises(ValidationError):
        ModerationResult(decision="no", reason="spam", user_id="usr1", business_id="bus1")

@pytest.mark.parametrize("text, expected", [
    ("The service was excellent and the meal was delicious.", "accept"),
    ("This food is badword1 awful!", "reject"),
    ("Ok", "flag")
], ids=["clean", "banned_word", "too_short"])
def test_moderate_custom(text, expected):
    review = ReviewRequest(user_id="usr1", business_id="bus1", text=text)
    result = moderate_custom(review)
    assert result["decision"] == expected

@pytest.mark.parametrize("text, expected", [
    ("The service was excellent and the meal was delicious.", "accept"),
    ("This food is damn awful!", "reject"),
    ("Ok", "flag")
], ids=["clean", "profanity", "too_short"])
def test_moderate_better_prof(text, expected):
    review = ReviewRequest(user_id="usr1", business_id="bus1", text=text)
    result = moderate_better_prof(review)
    assert result["decision"] == expected

