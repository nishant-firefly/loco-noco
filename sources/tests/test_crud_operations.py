import pytest
from .crud_operations import create_table, insert_data, fetch_data, update_data, delete_data


# Database connection details (same as in crud_operations.py)
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "test_db"
DB_USER = "test_user"
DB_PASSWORD = "test_password"

@pytest.fixture(scope="module")
def db_connection():
    """Fixture to establish a database connection."""
    import psycopg2
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    yield conn
    conn.close()

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Fixture to set up the database and table before tests."""
    create_table()
    yield

def test_insert_data(db_connection):
    """Test inserting data into the users table."""
    user_id = insert_data('Jane Doe', 'jane.doe@example.com', '0987654321')
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
    row = cursor.fetchone()
    assert row is not None
    assert row[1] == 'Jane Doe'
    assert row[2] == 'jane.doe@example.com'
    assert row[3] == '0987654321'

def test_fetch_data(db_connection):
    """Test fetching data from the users table."""
    rows = fetch_data()
    assert len(rows) > 0  # Ensure at least one row is fetched

def test_update_data(db_connection):
    """Test updating data in the users table."""
    user_id = insert_data('Alice Smith', 'alice.smith@example.com', '1112233445')
    update_data(user_id, name='Alice Johnson', phone='5556667778')
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
    row = cursor.fetchone()
    assert row[1] == 'Alice Johnson'
    assert row[3] == '5556667778'

def test_delete_data(db_connection):
    """Test deleting data from the users table."""
    user_id = insert_data('Bob Brown', 'bob.brown@example.com', '1234567890')
    delete_data(user_id)
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
    row = cursor.fetchone()
    assert row is None

