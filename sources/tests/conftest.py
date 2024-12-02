import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sources.tests.sample_data import Base, populate_sample_data

@pytest.fixture(scope="session")
def engine():
    """
    Fixture to create a SQLAlchemy engine for the PostgreSQL database.
    """
    from test_config import TEST_ENV_CONFIG

    postgres_config = TEST_ENV_CONFIG["services"]["postgres"]
    db_url = (
        f"postgresql://{postgres_config['environment']['POSTGRES_USER']}:"
        f"{postgres_config['environment']['POSTGRES_PASSWORD']}@localhost:"
        f"{list(postgres_config['ports'].keys())[0]}/"
        f"{postgres_config['environment']['POSTGRES_DB']}"
    )
    return create_engine(db_url)

@pytest.fixture(scope="session")
def setup_database(engine):
    """
    Fixture to set up the PostgreSQL database schema and populate it with data.
    """
    print("Setting up the PostgreSQL database schema...")
    Base.metadata.create_all(engine)  # Create all tables
    
    # Populate sample data
    Session = sessionmaker(bind=engine)
    session = Session()
    populate_sample_data(session)  # Populate data once
    session.commit()
    session.close()
    
    yield

    # Teardown: Drop tables after all tests
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(engine, setup_database):
    """
    Fixture to provide a new PostgreSQL session for each test.
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
