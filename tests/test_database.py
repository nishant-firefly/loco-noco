import sys
import os

# Ensure the root directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



import pytest
from config.database import get_session
from core.models.user import User

@pytest.fixture
def db_session():
    session = get_session("postgres")
    yield session
    session.close()

def test_database_connection(db_session):
    assert db_session is not None
