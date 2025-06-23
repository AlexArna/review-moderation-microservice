from app.custom_moderation import is_spam, moderate_custom
from app.better_prof_moderation import moderate_better_prof
from app.models import ReviewRequest

def test_is_spam_promotion():
    assert is_spam("Buy now this amazing opportunity!")

def test_is_spam_clickbait():
    assert is_spam("Click here to get rich quick!")

def test_is_spam_too_short():
    assert is_spam("Ok")

def test_is_spam_too_long():
    assert is_spam("The service was excellent and the meal was delicious." * 10)

def test_is_spam_clean():
    assert not is_spam("The service was excellent and the meal was delicious.")

def test_custom_moderation_clean():
    review = ReviewRequest(user_id="usr1", business_id="bus1", text="The service was excellent and the meal was delicious.")
    result = moderate_custom(review)
    assert result["decision"] == "accept"

def test_custom_moderation_profane():
    review = ReviewRequest(user_id="usr1", business_id="bus1", text="This food is badword1 awful!")
    result = moderate_custom(review)
    assert result["decision"] == "reject"

def test_custom_moderation_spam_too_short():
    review = ReviewRequest(user_id="usr1", business_id="bus1", text="Ok")
    result = moderate_custom(review)
    assert result["decision"] == "flag"

def test_better_prof_moderation_clean():
    review = ReviewRequest(user_id="usr1", business_id="bus1", text="The service was excellent and the meal was delicious.")
    result = moderate_better_prof(review)
    assert result["decision"] == "accept"

def test_better_prof_moderation_profane():
    review = ReviewRequest(user_id="usr1", business_id="bus1", text="This food is damn awful!")
    result = moderate_better_prof(review)
    assert result["decision"] == "reject"

def test_better_prof_moderation_spam_too_short():
    review = ReviewRequest(user_id="usr1", business_id="bus1", text="Ok")
    result = moderate_better_prof(review)
    assert result["decision"] == "flag"
