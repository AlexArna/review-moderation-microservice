from fastapi import FastAPI, HTTPException
from app.models import ReviewRequest, ModerationResult
from app.moderation import moderate_review

app = FastAPI(
    title="Review Moderation Microservice",
    description="API to moderate reviews for spam, profanity, and more.",
    version="0.1.0"
)

@app.post("/reviews", response_model=ModerationResult)
async def submit_review(review: ReviewRequest):
    result = moderate_review(review)
    return result

@app.get("/")
def read_root():
    return {"message": "Review Moderation Microservice up and running!"}