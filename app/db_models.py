from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime

# Create a base class for all SQLAlchemy models
Base = declarative_base()

# Define a new table called moderation_events
# Each instance of ModerationEvent is a row in the table
class ModerationEvent(Base):
    """
    SQLAlchemy ORM model for storing moderation events/results for each review.
    Tracks who submitted, what was reviewed, the moderation outcome, and which method was used.
    """
    __tablename__ = "moderation_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    business_id = Column(String, index=True)
    review_text = Column(String)
    moderation_result = Column(String) # accept/flag/reject
    moderation_reason = Column(String) # spam, profanity, clean
    method_used = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))