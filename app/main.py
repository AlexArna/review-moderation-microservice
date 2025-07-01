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
from datetime import datetime
from app.kafka_client import get_kafka_producer
from functools import lru_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Review Moderation Microservice",
    description="API to moderate reviews for spam and profanity",
    version="0.4.0"
)

# Ensures that only one instance of the producer is created (singleton)
@lru_cache()
def get_producer():
    return get_kafka_producer()

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
    db: Session = Depends(get_db),
    producer=Depends(get_producer)
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

        # Publish the moderation event to Kafka
        kafka_event = {
            "id": event.id,
            "user_id": event.user_id,
            "business_id": event.business_id,
            "review_text": event.review_text,
            "moderation_result": event.moderation_result,
            "moderation_reason": event.moderation_reason,
            "method_used": event.method_used,
            # Use event.timestamp if available, otherwise fallback to now
            "timestamp": (event.timestamp.isoformat() if hasattr(event, "timestamp") and event.timestamp else datetime.utcnow().isoformat())
        }
        producer.send("moderation-events", kafka_event)
        producer.flush()  # For reliability

    except Exception as e:
        logger.exception("Moderation service error")
        raise HTTPException(status_code=500, detail="Moderation service error.")
    return result

@app.get("/", tags=["Info"])
def read_root():
    """Return a welcome message confirming the service is running."""
    return {"message": "Review Moderation Microservice up and running!"}

@app.get("/moderation-events", tags=["Analytics"])
def list_events(
    limit: int = Query(100, description="Max events to return"),
    db: Session = Depends(get_db)
):
    """
    List moderation events for analytics or downstream processing.
    """
    events = db.query(ModerationEvent).order_by(ModerationEvent.timestamp.desc()).limit(limit).all()
    # Convert SQLAlchemy objects to dicts for JSON response
    return [
        {
            "id": e.id,
            "user_id": e.user_id,
            "business_id": e.business_id,
            "review_text": e.review_text,
            "moderation_result": e.moderation_result,
            "moderation_reason": e.moderation_reason,
            "method_used": e.method_used,
            "timestamp": e.timestamp.isoformat() if e.timestamp else None
        }
        for e in events
    ]