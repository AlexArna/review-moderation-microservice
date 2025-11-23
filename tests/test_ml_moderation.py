import pytest
from unittest.mock import patch, MagicMock
import app.tfidf_logreg_moderation as tfidf_mod
from app.models import ReviewRequest

@pytest.mark.parametrize("text, ml_label, expected_decision, expected_reason", [
    ("The service was excellent and the meal was delicious.", "clean", "accept", "no profanity or spam detected"),
    ("This food is damn awful!", "profanity", "reject", "contains profanity (ML detected)"),
    ("Ok", "spam", "flag", "flagged for suspected spam (ML detected)"),
    ("WELL!!???The food was average...@", "unknown_label", "flag", "unrecognized label"),
    ("The service was excellent and the meal was delicious.", [], "flag", "empty label")
], ids=["clean", "profanity", "too_short", "unrecognized_label", "empty_list"])
@patch.object(tfidf_mod, "model") # create a mock object for model
def test_moderate_tfidf_logreg(mock_model, text, ml_label, expected_decision, expected_reason):
    # simulate model prediction, including when the model returns an empty list
    mock_model.predict.return_value = [] if isinstance(ml_label, list) else [ml_label]
    review = ReviewRequest(user_id="usr1", business_id="bus1", text=text)
    result = tfidf_mod.moderate_tfidf_logreg(review)
    assert result["decision"] == expected_decision
    assert result["reason"] == expected_reason

# Model fails to load
@patch.object(tfidf_mod, "model", new=None)
def test_exception_raised_when_model_fails_to_load():
    review = ReviewRequest(user_id="usr1", business_id="bus1", text="Amazing food!")
    result = tfidf_mod.moderate_tfidf_logreg(review)
    assert result["decision"] == "flag"
    assert result["reason"] == "model exception"

# Model fails to predict
@pytest.mark.parametrize("exception_type, expected_decision, expected_reason",[
    (OSError("Could not open file"), "flag", "model exception"),
    (FileNotFoundError("No such model file"), "flag", "model exception"),
    (RuntimeError("General loading failure"), "flag", "model exception" )
], ids=["ose_error", "file_not_found", "runtime_error"])
@patch.object(tfidf_mod, "model")
def test_exception_caught_when_prediction_fails(mock_model, exception_type, expected_decision, expected_reason):
    mock_model.predict.side_effect = exception_type
    review = ReviewRequest(user_id="usr1", business_id="bus1", text="Amazing food!")
    result = tfidf_mod.moderate_tfidf_logreg(review)
    assert result["decision"] == expected_decision
    assert result["reason"] == expected_reason
    
# Model predicts an empty list
@patch.object(tfidf_mod, "model")
def test_model_returns_empty_list(mock_model):
    mock_model.predict.return_value = []
    review = ReviewRequest(user_id="usr1", business_id="bus1", text="Amazing food!")
    result = tfidf_mod.moderate_tfidf_logreg(review)
    assert result["decision"] == "flag"
    assert result["reason"] == "empty label"
    
# Model predicts unknown label
@patch.object(tfidf_mod, "model")
def test_model_predicts_unknown_label(mock_model):
    mock_model.predict.return_value = ["weird label"]
    review = ReviewRequest(user_id="usr1", business_id="bus1", text="Amazing food!")
    result = tfidf_mod.moderate_tfidf_logreg(review)
    assert result["decision"] == "flag"
    assert result["reason"] == "unrecognized label"

@pytest.mark.xfail(reason="moderate_tfidf_logreg() catches exceptions instead of raising them")
@patch.object(tfidf_mod, "model")
def test_exception_not_raised_when_prediction_fails(mock_model):
    # raise an exception when the model is called
    mock_model.predict.side_effect = RuntimeError("Failed to load the model")
    review = ReviewRequest(user_id="usr1", business_id="bus1", text="Amazing food!")
    with pytest.raises(RuntimeError):
        tfidf_mod.moderate_tfidf_logreg(review)

