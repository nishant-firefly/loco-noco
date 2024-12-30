from app.database import engine
from app.models.models import Base  # Import Base from models file

# Create all tables defined in models.py
def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Tables created successfully.")
