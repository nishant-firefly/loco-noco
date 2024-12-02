import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sources.tests.sample_data import Base, populate_sample_data

@pytest.fixture(scope="session")
def engine():
    """
    Fixture to create a SQLAlchemy engine for an in-memory SQLite database.
    """
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="session")
def setup_database(engine):
    """
    Fixture to set up the database schema and populate it with data.
    """
    print("Setting up the database schema...")
    Base.metadata.create_all(engine)  # Create all tables
    yield
    Base.metadata.drop_all(engine)  # Drop all tables after the session ends

@pytest.fixture(scope="function")
def db_session(engine, setup_database):
    """
    Fixture to provide a new database session for each test.
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    # Populate the database with sample data
    populate_sample_data(session)
    session.commit()

    yield session

    session.close()
