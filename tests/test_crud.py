import sys
import os

# Ensure the root directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))





import pytest
from config.database import get_session
from core.repositories.user_repo import UserRepository
from core.models.user import User

@pytest.fixture
def db_session():
    session = get_session("postgres")
    yield session
    session.close()

@pytest.fixture
def user_repo(db_session):
    return UserRepository(db_session)

def test_create_user(user_repo):
    new_user = user_repo.create(User, {"name": "Test User", "email": "test@example.com"})
    assert new_user.id is not None
    assert new_user.name == "Test User"
    assert new_user.email == "test@example.com"

def test_read_user(user_repo):
    user = user_repo.get_user_by_email("test@example.com")
    assert user is not None
    assert user.email == "test@example.com"

def test_update_user(user_repo):
    user = user_repo.get_user_by_email("test@example.com")
    updated_user = user_repo.update(User, user.id, {"name": "Updated User"})
    assert updated_user.name == "Updated User"

def test_delete_user(user_repo):
    user = user_repo.get_user_by_email("test@example.com")
    deleted = user_repo.delete(User, user.id)
    assert deleted is True
