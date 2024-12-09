import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sources.rdbms.sources.generic_rdbms_source import GenericRDBMSSource
from .sample_data import Base, User, Permission, populate_sample_data

@pytest.fixture
def source(db_session):
    """
    Fixture to initialize GenericRDBMSSource using the PostgreSQL db_session.
    """
    return GenericRDBMSSource(db_session.bind.url)  # Pass the PostgreSQL engine URL


@pytest.fixture
def source(db_session):
    """Fixture to initialize GenericRDBMSSource."""
    return GenericRDBMSSource("sqlite:///:memory:")

def test_filter(source, db_session):
    """Test filtering data."""
    with db_session() as session:
        users = source.filter(User, {"name": "John Doe"})
        assert len(users) == 1
        assert users[0].email == "john.doe@example.com"

def test_update(source, db_session):
    """Test updating data."""
    with db_session() as session:
        user = source.filter(User, {"name": "Jane Smith"})[0]
        source.update(User, user.id, {"email": "updated.email@example.com"})

        # Verify the update
        updated_user = source.filter(User, {"id": user.id})[0]
        assert updated_user.email == "updated.email@example.com"

def test_delete(source, db_session):
    """Test deleting data."""
    with db_session() as session:
        user = source.filter(User, {"name": "John Doe"})[0]
        source.delete(User, user.id)

        # Verify deletion
        deleted_user = source.filter(User, {"id": user.id})
        assert len(deleted_user) == 0

def test_permission_json(source, db_session):
    """Test permissions with JSON-based structure."""
    with db_session() as session:
        permissions = source.filter(Permission, {"entity_name": "users"})
        assert len(permissions) == 1
        assert permissions[0].permission_json["create"] is True
        assert permissions[0].permission_json["update"] is False