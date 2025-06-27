from fastapi import FastAPI, HTTPException, Query, Depends
from app.models import ReviewRequest, ModerationResult
from app.custom_moderation import moderate_custom
from app.better_prof_moderation import moderate_better_prof
from app.tfidf_logreg_moderation import moderate_tfidf_logreg
from app.tinyBert_moderation import moderate_tinybert
from sqlalchemy.orm import Session
from app.db_session import get_db
from app.db_models import ModerationEvent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Review Moderation Microservice",
    description="API to moderate reviews for spam and profanity",
    version="0.3.0"
)

@app.post(
    "/reviews",
    response_model=ModerationResult,
    tags=["Moderation"],
    summary="Moderate a user review",
    operation_id="moderateReview",
    responses={
        400: {"description": "Invalid input or moderation method."},
        500: {"description": "Server error."}
    }
)
async def submit_review(
    review: ReviewRequest,
    method: str = Query(
        "better_prof", 
        enum=["custom", "better_prof", "ml", "tinybert"], 
        description="Choose 'custom' for custom banned words and spam rules, 'better_prof' for rule-based profanity moderation, 'ml' for machine learning moderation (tf-idf + logistic regression), or 'tinybert' for Transformer-based moderation (TinyBERT)."
    ),
    db: Session = Depends(get_db)
):
    """
    Moderate a review using one of several moderation backends:

    - **custom**: Uses your own banned words and simple spam rules.
    - **better_prof**: Uses the better_profanity wordlist (rule-based) and simple spam rules (default).
    - **ml**: Uses tf-idf and logistic regression. 
    - **tinybert**: Uses the TinyBERT Transformer model.

    Example: POST /reviews?method=custom
    """
    try:
        if method == "custom":
            result = moderate_custom(review)
        elif method == "better_prof":
            result = moderate_better_prof(review)
        elif method == "ml":
            result = moderate_tfidf_logreg(review)
        elif method == "tinybert":
            result = moderate_tinybert(review)
        else:
            raise HTTPException(status_code=400, detail="Invalid moderation method.")

        # Store the moderation event in the database
        event = ModerationEvent(
            user_id=review.user_id,
            business_id=review.business_id,
            review_text=review.text,
            moderation_result=result["decision"],
            moderation_reason=result["reason"],
            method_used=method
        )
        db.add(event)
        db.commit()
        db.refresh(event)

    except Exception as e:
        logger.exception("Moderation service error")
        raise HTTPException(status_code=500, detail="Moderation service error.")
    return result

@app.get("/", tags=["Info"])
def read_root():
    """Return a welcome message confirming the service is running."""
    return {"message": "Review Moderation Microservice up and running!"}
