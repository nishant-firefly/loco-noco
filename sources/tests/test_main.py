import pytest
from sources.rdbms.helpers.rdbms_helper import RDBMSHelper
from sources.rdbms.sources.postgres_source import PostgresSource
from sources.rdbms.models.models import Base, User
from sources.tests.test_config import TEST_ENV_CONFIG
import pandas as pd
from sqlalchemy.sql import text  # Import the text function

# Configure database URL from test config
postgres_config = TEST_ENV_CONFIG["services"]["postgres"]
DB_URL = (
    f"postgresql://{postgres_config['environment']['POSTGRES_USER']}:"
    f"{postgres_config['environment']['POSTGRES_PASSWORD']}@localhost:"
    f"{list(postgres_config['ports'].keys())[0]}/"
    f"{postgres_config['environment']['POSTGRES_DB']}"
)

db_helper = RDBMSHelper(DB_URL)
db_source = PostgresSource(DB_URL)

# Ensure tables are created before tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    db_helper.create_all_tables(Base)
    yield
    db_helper.drop_all_tables(Base)

@pytest.fixture(autouse=True)
def clear_users_table():
    """Clear the users table before each test."""
    with db_source.Session() as session:
        # Use text() to wrap raw SQL statement
        session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
        session.commit()

def test_create_users_from_csv(tmp_path):
    # Prepare test data
    test_csv_path = tmp_path / "test_users.csv"
    test_data = [
        {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"},
    ]
    pd.DataFrame(test_data).to_csv(test_csv_path, index=False)

    # Insert users
    for row in test_data:
        db_source.create(User, row)

    # Validate users are created
    for row in test_data:
        user = db_source.read(User, row["id"])
        assert user.name == row["name"]
        assert user.email == row["email"]

def test_read_user():
    user_data = {"id": 10, "name": "Alice Wonderland", "email": "alice@example.com"}
    db_source.create(User, user_data)

    user = db_source.read(User, 10)
    assert user.name == user_data["name"]
    assert user.email == user_data["email"]

def test_update_user():
    user_data = {"id": 20, "name": "Old Name", "email": "old@example.com"}
    db_source.create(User, user_data)

    update_data = {"name": "New Name", "email": "new@example.com"}
    db_source.update(User, 20, update_data)

    user = db_source.read(User, 20)
    assert user.name == "New Name"
    assert user.email == "new@example.com"

def test_delete_user():
    user_data = {"id": 30, "name": "Delete Me", "email": "delete@example.com"}
    db_source.create(User, user_data)

    db_source.delete(User, 30)
    user = db_source.read(User, 30)
    assert user is None

def test_export_users_to_csv(tmp_path):
    user_data = [
        {"id": 40, "name": "User A", "email": "usera@example.com"},
        {"id": 50, "name": "User B", "email": "userb@example.com"},
    ]
    for row in user_data:
        db_source.create(User, row)

    output_csv_path = tmp_path / "exported_users.csv"
    users = db_source.filter(User, {})
    user_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    pd.DataFrame(user_list).to_csv(output_csv_path, index=False)

    exported_data = pd.read_csv(output_csv_path)
    for i, row in enumerate(user_data):
        assert exported_data.iloc[i]["id"] == row["id"]
        assert exported_data.iloc[i]["name"] == row["name"]
        assert exported_data.iloc[i]["email"] == row["email"]
