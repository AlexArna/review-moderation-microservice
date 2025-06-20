from pydantic import BaseModel

class ReviewRequest(BaseModel):
    user_id: str
    business_id: str
    text: str

class ModerationResult(BaseModel):
    decision: str  # "accept", "flag", "reject"
    reason: str
    user_id: str
    business_id: str