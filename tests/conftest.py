# Shared fixtures for pytest
import pytest
from src.helpers.rdbms_helper import RDBMSHelper
from src.models.models import Base

DB_URL = "postgresql://test_user:test_password@localhost:5432/test_db"

@pytest.fixture(scope="module")
def db_helper():
    """
    Fixture to provide a database helper instance and manage schema setup/teardown.
    """
    helper = RDBMSHelper(DB_URL)
    
    # Create all tables at the start of the test module
    helper.create_all_tables(Base)
    
    yield helper  # Provide the helper to the test functions
    
    # Drop all tables after the test module finishes
    helper.drop_all_tables(Base)
