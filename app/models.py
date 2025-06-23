from pydantic import BaseModel, Field
from enum import Enum


class ModerationDecision(str, Enum):
    accept = "accept"
    flag = "flag"
    reject = "reject"

class ReviewRequest(BaseModel):
    user_id: str = Field(..., description="ID of the user submitting the review.", json_schema_extra={"example": "usr1"})
    business_id: str = Field(..., description="ID of the business being reviewed.", json_schema_extra={"example": "bus1"})
    text: str = Field(..., description="The text of the user's review.", json_schema_extra={"example": "The food was amazing!"})

class ModerationResult(BaseModel):
    decision: ModerationDecision = Field(..., description="Decision on the review.", json_schema_extra={"example": "accept"})
    reason: str = Field(..., description="Reason for the decision.", json_schema_extra={"example": "Contains profanity"})
    user_id: str = Field(..., description="ID of the user submitting the review.", json_schema_extra={"example": "usr1"})
    business_id: str = Field(..., description="ID of the business being reviewed.", json_schema_extra={"example": "bus1"})