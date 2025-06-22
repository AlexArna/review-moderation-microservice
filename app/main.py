from fastapi import FastAPI, HTTPException, Query
from app.models import ReviewRequest, ModerationResult
from app.custom_moderation import moderate_custom
from app.better_prof_moderation import moderate_better_prof

app = FastAPI(
    title="Review Moderation Microservice",
    description="API to moderate reviews for spam, profanity, and more.",
    version="0.2.0"
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
        enum=["custom", "better_prof"], 
        description="Choose 'custom' for custom banned words and spam rules, or 'better_prof' for rule-based profanity moderation."
    )
):
    """
    Moderate a review using either a custom banned-words filter or the better_profanity wordlist.

    - **custom**: Uses your own banned words and simple spam rules.
    - **better_prof**: Uses the better_profanity wordlist (rule-based) and simple spam rules (default).

    Example: POST /reviews?method=custom
    """
    try:
        if method == "custom":
            result = moderate_custom(review)
        elif method == "better_prof":
            result = moderate_better_prof(review)
        else:
            raise HTTPException(status_code=400, detail="Invalid moderation method.")
    except Exception:
        raise HTTPException(status_code=500, detail="Moderation service error.")
    return result

@app.get("/", tags=["Info"])
def read_root():
    """Welcomes the user with a message confirming the service is running."""
    return {"message": "Review Moderation Microservice up and running!"}
