from .database import SessionLocal

def get_db():
    """
    Dependency that provides a SQLAlchemy database session.
    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db  # Provide the session to the endpoint
    finally:
        db.close()  # Close the session when done