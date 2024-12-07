import psycopg2
from psycopg2 import sql

# Database connection details
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "test_db"
DB_USER = "test_user"
DB_PASSWORD = "test_password"

def connect_db():
    """Create a connection to the PostgreSQL database."""
    try:
        print(f"Connecting to the database {DB_NAME} at {DB_HOST}:{DB_PORT}...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connection successful!")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Connection error: {e}")
        raise

def create_table():
    """Create a table in the database."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                phone VARCHAR(15)
            );
        """)
        conn.commit()
        print("Table created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()

def insert_data(name, email, phone):
    """Insert data into the table."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (name, email, phone) 
            VALUES (%s, %s, %s)
            RETURNING id;
        """, (name, email, phone))
        user_id = cursor.fetchone()[0]
        conn.commit()
        print(f"Data inserted: {name}, {email}, {phone}")
        return user_id
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def fetch_data():
    """Fetch all data from the users table."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def update_data(user_id, name=None, email=None, phone=None):
    """Update data in the users table."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Dynamically build the SET clause based on provided values
        fields = []
        values = []

        if name is not None:
            fields.append("name = %s")
            values.append(name)
        if email is not None:
            fields.append("email = %s")
            values.append(email)
        if phone is not None:
            fields.append("phone = %s")
            values.append(phone)

        # Ensure we have something to update
        if not fields:
            raise ValueError("No fields provided to update.")

        query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s;"
        values.append(user_id)  # Add user_id as the last parameter
        cursor.execute(query, tuple(values))
        conn.commit()
        print(f"Data updated for user ID {user_id}")
    except Exception as e:
        print(f"Error updating data: {e}")
        conn.rollback()  # Rollback changes in case of an error
    finally:
        cursor.close()
        conn.close()

def delete_data(user_id):
    """Delete data from the table."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
        print(f"Data deleted for user ID {user_id}")
    except Exception as e:
        print(f"Error deleting data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

