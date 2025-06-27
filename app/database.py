from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set the SQLite database URL in the current directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./moderation.db"

# Create the database engine (connection)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # Required for SQLite when used with FastAPI due to threading
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)