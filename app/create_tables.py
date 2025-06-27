from .database import engine
from .db_models import Base  # Base = declarative_base()

# Creates all tables that are defined as subclasses of Base
Base.metadata.create_all(bind=engine)