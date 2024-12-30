import pytest
from app.database import get_db, engine
from app.models.models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config.test_config import TEST_ENV_CONFIG
import psycopg2
import time

# Create a session for the database
@pytest.fixture(scope="session")
def db_session():
    # Set up the database connection URL from the test config
    db_config = TEST_ENV_CONFIG["services"]["postgres"]["environment"]
    DATABASE_URL = f"postgresql://{db_config['POSTGRES_USER']}:{db_config['POSTGRES_PASSWORD']}@localhost:{5432}/{db_config['POSTGRES_DB']}"

    # Create a new engine for testing purposes
    engine = create_engine(DATABASE_URL, echo=True)
    
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    
    # Set up a sessionmaker for database interactions
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create a session and yield it to the test functions
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the tests are done
        Base.metadata.drop_all(bind=engine)

# Helper function to check if PostgreSQL is ready
def wait_for_postgres():
    db_config = TEST_ENV_CONFIG["services"]["postgres"]["environment"]
    while True:
        try:
            # Try connecting to the PostgreSQL container
            conn = psycopg2.connect(
                dbname=db_config["POSTGRES_DB"],
                user=db_config["POSTGRES_USER"],
                password=db_config["POSTGRES_PASSWORD"],
                host="localhost",
                port=5432
            )
            conn.close()
            break
        except psycopg2.OperationalError:
            print("PostgreSQL is not ready. Retrying...")
            time.sleep(5)

# Wait for PostgreSQL to be ready before running the tests
wait_for_postgres()
