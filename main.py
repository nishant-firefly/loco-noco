import pandas as pd
from sources.rdbms.sources.postgres_source import PostgresSource
from sources.rdbms.models.models import Base, User
from sources.rdbms.helpers.rdbms_helper import RDBMSHelper
from sources.tests.test_config import TEST_ENV_CONFIG

# Step 1: Configure DB_URL from test_config.py
postgres_config = TEST_ENV_CONFIG["services"]["postgres"]
DB_URL = (
    f"postgresql://{postgres_config['environment']['POSTGRES_USER']}:"
    f"{postgres_config['environment']['POSTGRES_PASSWORD']}@localhost:"
    f"{list(postgres_config['ports'].keys())[0]}/"
    f"{postgres_config['environment']['POSTGRES_DB']}"
)

# Step 2: Initialize RDBMS helper and Postgres source
db_helper = RDBMSHelper(DB_URL)
db_source = PostgresSource(DB_URL)

# Step 3: Ensure tables are created
db_helper.create_all_tables(Base)


def create_users_from_csv(csv_path):
    """
    Create users in the database from a CSV file.

    Args:
        csv_path (str): Path to the input CSV file.
    """
    try:
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            user_data = {"name": row["name"], "email": row["email"]}
            db_source.create(User, user_data)
        print("Users successfully created from CSV!")
    except Exception as e:
        print(f"Error creating users from CSV: {e}")


def read_user(user_id):
    """
    Read a user from the database by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
    """
    try:
        user = db_source.read(User, user_id)
        if user:
            print(f"User Found: ID={user.id}, Name={user.name}, Email={user.email}")
        else:
            print("User not found.")
    except Exception as e:
        print(f"Error reading user: {e}")


def update_user(user_id, update_fields):
    """
    Update a user's information.

    Args:
        user_id (int): ID of the user to update.
        update_fields (dict): Fields to update with their new values.
    """
    try:
        db_source.update(User, user_id, update_fields)
        print(f"User with ID={user_id} successfully updated.")
    except Exception as e:
        print(f"Error updating user: {e}")


def delete_user(user_id):
    """
    Delete a user from the database.

    Args:
        user_id (int): ID of the user to delete.
    """
    try:
        db_source.delete(User, user_id)
        print(f"User with ID={user_id} successfully deleted.")
    except Exception as e:
        print(f"Error deleting user: {e}")


def export_users_to_csv(output_path):
    """
    Export all users to a CSV file.

    Args:
        output_path (str): Path to save the CSV file.
    """
    try:
        users = db_source.filter(User, {})
        user_data = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
        df = pd.DataFrame(user_data)
        df.to_csv(output_path, index=False)
        print(f"Users exported to {output_path}")
    except Exception as e:
        print(f"Error exporting users to CSV: {e}")


if __name__ == "__main__":
    # Step 4: Paths for input and output CSV
    input_csv = "D:/workspace/nishant/loco-noco/data/users.csv"
    output_csv = "D:/workspace/nishant/loco-noco/data/exported_users.csv"

    # Step 5: Perform CRUD operations
    print("Creating users from CSV...")
    create_users_from_csv(input_csv)

    print("\nReading a user with ID=1...")
    read_user(1)

    print("\nUpdating a user with ID=2...")
    update_user(2, {"name": "Updated User", "email": "updated.email@example.com"})

    print("\nDeleting a user with ID=39...")
    delete_user(39)

    print("\nExporting users to a new CSV...")
    export_users_to_csv(output_csv)
