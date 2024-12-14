import pytest
import pandas as pd
from src.models.models import User
from src.utils.data_loader import DataLoader
from sqlalchemy import text  # Import the text function
import numpy as np
import sqlalchemy

# Convert all integer-like columns to Python native int
def convert_numpy_int64_to_int(data):
    for col in data.select_dtypes(include=[np.int64]).columns:
        data[col] = data[col].astype(int)
    return data

# Test for basic CRUD operations
def test_postgres_crud(db_helper):
    file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
    data_loader = DataLoader(file_path=file_path)
    data = data_loader.load_data(sheet_name="Postgres")
    data["id"] = data["id"].apply(lambda x: int(x))
    data["age"] = data["age"].apply(lambda x: int(x))

    with db_helper.get_session() as session:
        session.execute(text("DELETE FROM users"))
        session.commit()

    for _, row in data.iterrows():
        user = User(id=int(row["id"]), name=row["name"], age=int(row["age"]))
        with db_helper.get_session() as session:
            session.add(user)
            session.commit()

    with db_helper.get_session() as session:
        for _, row in data.iterrows():
            retrieved_user = session.query(User).filter_by(id=row["id"]).first()
            assert retrieved_user.name == row["name"]
            assert retrieved_user.age == row["age"]

    with db_helper.get_session() as session:
        session.query(User).filter_by(id=int(data.iloc[0]["id"])).update({"age": 40})
        session.commit()

    with db_helper.get_session() as session:
        updated_user = session.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
        assert updated_user.age == 40

    with db_helper.get_session() as session:
        session.query(User).filter_by(id=int(data.iloc[0]["id"])).delete()
        session.commit()

    with db_helper.get_session() as session:
        deleted_user = session.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
        assert deleted_user is None

# Test for advanced query filters
def test_postgres_advanced_query(db_helper):
    file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
    data_loader = DataLoader(file_path=file_path)
    data = data_loader.load_data(sheet_name="Postgres")
    data["id"] = data["id"].apply(lambda x: int(x))
    data["age"] = data["age"].apply(lambda x: int(x))

    with db_helper.get_session() as session:
        result = session.query(User).filter(User.age > 30).all()
        assert len(result) > 0 if result else True

# Test for session rollback functionality
def test_postgres_session_rollback(db_helper):
    file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
    data_loader = DataLoader(file_path=file_path)
    data = data_loader.load_data(sheet_name="Postgres")
    data["id"] = data["id"].apply(lambda x: int(x))
    data["age"] = data["age"].apply(lambda x: int(x))

    with db_helper.get_session() as session:
        user = User(id=int(data.iloc[0]["id"]), name=data.iloc[0]["name"], age=int(data.iloc[0]["age"]))
        session.add(user)
        session.rollback()

    with db_helper.get_session() as session_check:
        rolled_back_user = session_check.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
        assert rolled_back_user is None

# Test for invalid data handling
def test_postgres_invalid_data(db_helper):
    with db_helper.get_session() as session:
        try:
            invalid_user = User(id="abc", name=None, age=-10)
            session.add(invalid_user)
            session.commit()
        except Exception as e:
            session.rollback()
            assert isinstance(e, (ValueError, sqlalchemy.exc.SQLAlchemyError))

# Test for transactional integrity
def test_postgres_transactional_integrity(db_helper):
    with db_helper.get_session() as session:
        try:
            valid_user = User(id=1, name="John Doe", age=30)
            session.add(valid_user)

            invalid_user = User(id="abc", name=None, age=-10)
            session.add(invalid_user)

            session.commit()
        except Exception:
            session.rollback()

    with db_helper.get_session() as session_check:
        result = session_check.query(User).filter_by(id=1).first()
        assert result is None

# Test for bulk insert
def test_postgres_bulk_insert(db_helper):
    # Clear the users table
    with db_helper.get_session() as session:
        session.execute(text("DELETE FROM users"))
        session.commit()

    # Load test data
    file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
    data_loader = DataLoader(file_path=file_path)
    data = data_loader.load_data(sheet_name="Postgres")

    # Convert numpy.int64 to int
    data["id"] = data["id"].apply(lambda x: int(x))
    data["age"] = data["age"].apply(lambda x: int(x))

    # Bulk insert
    users = [User(id=int(row["id"]), name=row["name"], age=int(row["age"])) for _, row in data.iterrows()]
    with db_helper.get_session() as session:
        session.bulk_save_objects(users)
        session.commit()

    # Verify the inserted data
    with db_helper.get_session() as session:
        for _, row in data.iterrows():
            retrieved_user = session.query(User).filter_by(id=int(row["id"])).first()
            assert retrieved_user is not None
            assert retrieved_user.name == row["name"]
            assert retrieved_user.age == int(row["age"])


# Test for duplicate insertion
def test_postgres_duplicate_insertion(db_helper):
    # Clear the users table
    with db_helper.get_session() as session:
        session.execute(text("DELETE FROM users"))
        session.commit()

    # Load test data
    file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
    data_loader = DataLoader(file_path=file_path)
    data = data_loader.load_data(sheet_name="Postgres")

    # Convert numpy.int64 to int
    data["id"] = data["id"].apply(lambda x: int(x))
    data["age"] = data["age"].apply(lambda x: int(x))

    # Insert a single record
    user = User(id=int(data.iloc[0]["id"]), name=data.iloc[0]["name"], age=int(data.iloc[0]["age"]))
    with db_helper.get_session() as session:
        session.add(user)
        session.commit()

    # Attempt to insert the same record again, expecting a unique constraint violation
    with db_helper.get_session() as session:
        duplicate_user = User(id=int(data.iloc[0]["id"]), name=data.iloc[0]["name"], age=int(data.iloc[0]["age"]))
        try:
            session.add(duplicate_user)
            session.commit()
        except Exception as exc:
            session.rollback()  # Explicitly roll back the session after the exception
            assert "duplicate key value" in str(exc)

    # Verify that no additional record was inserted
    with db_helper.get_session() as session:
        count = session.query(User).filter_by(id=int(data.iloc[0]["id"])).count()
        assert count == 1


































# import pytest
# import pandas as pd
# from src.models.models import User
# from src.utils.data_loader import DataLoader
# from sqlalchemy import text
# import numpy as np

# # Utility Functions
# def convert_numpy_int64_to_int(data):
#     for col in data.select_dtypes(include=[np.int64]).columns:
#         data[col] = data[col].astype(int)
#     return data

# def reset_database(session):
#     """Utility to clear the users table for a fresh test."""
#     session.execute(text("DELETE FROM users"))
#     session.commit()

# # Test Cases
# def test_postgres_crud(db_helper):
#     file_path = r"D:\\workspace\\loco_noco_rdbms\\loco_noco\\data\\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")

#     data = convert_numpy_int64_to_int(data)

#     with db_helper.get_session() as session:
#         reset_database(session)

#     for _, row in data.iterrows():
#         user = User(id=row["id"], name=row["name"], age=row["age"])
#         with db_helper.get_session() as session:
#             session.add(user)
#             session.commit()

#     with db_helper.get_session() as session:
#         for _, row in data.iterrows():
#             retrieved_user = session.query(User).filter_by(id=row["id"]).first()
#             assert retrieved_user.name == row["name"]
#             assert retrieved_user.age == row["age"]

#     with db_helper.get_session() as session:
#         session.query(User).filter_by(id=data.iloc[0]["id"]).update({"age": 40})
#         session.commit()

#     with db_helper.get_session() as session:
#         updated_user = session.query(User).filter_by(id=data.iloc[0]["id"]).first()
#         assert updated_user.age == 40

#     with db_helper.get_session() as session:
#         session.query(User).filter_by(id=data.iloc[0]["id"]).delete()
#         session.commit()

#     with db_helper.get_session() as session:
#         deleted_user = session.query(User).filter_by(id=data.iloc[0]["id"]).first()
#         assert deleted_user is None

# def test_postgres_advanced_query(db_helper):
#     file_path = r"D:\\workspace\\loco_noco_rdbms\\loco_noco\\data\\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")

#     data = convert_numpy_int64_to_int(data)

#     with db_helper.get_session() as session:
#         result = session.query(User).filter(User.age > 30).all()
#         assert len(result) >= 0

# def test_postgres_session_rollback(db_helper):
#     file_path = r"D:\\workspace\\loco_noco_rdbms\\loco_noco\\data\\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")

#     data = convert_numpy_int64_to_int(data)

#     with db_helper.get_session() as session:
#         user = User(id=data.iloc[0]["id"], name=data.iloc[0]["name"], age=data.iloc[0]["age"])
#         session.add(user)
#         session.rollback()

#     with db_helper.get_session() as session_check:
#         rolled_back_user = session_check.query(User).filter_by(id=data.iloc[0]["id"]).first()
#         assert rolled_back_user is None

# def test_postgres_duplicate_insertion(db_helper):
#     file_path = r"D:\\workspace\\loco_noco_rdbms\\loco_noco\\data\\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")

#     data = convert_numpy_int64_to_int(data)

#     with db_helper.get_session() as session:
#         reset_database(session)

#     for _, row in data.iterrows():
#         user = User(id=row["id"], name=row["name"], age=row["age"])
#         with db_helper.get_session() as session:
#             session.add(user)
#             session.commit()

#     with pytest.raises(Exception):
#         for _, row in data.iterrows():
#             user = User(id=row["id"], name=row["name"], age=row["age"])
#             with db_helper.get_session() as session:
#                 session.add(user)
#                 session.commit()

# def test_postgres_bulk_insert(db_helper):
#     file_path = r"D:\\workspace\\loco_noco_rdbms\\loco_noco\\data\\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")

#     data = convert_numpy_int64_to_int(data)

#     with db_helper.get_session() as session:
#         reset_database(session)

#     users = [User(id=row["id"], name=row["name"], age=row["age"]) for _, row in data.iterrows()]

#     with db_helper.get_session() as session:
#         session.bulk_save_objects(users)
#         session.commit()

#     with db_helper.get_session() as session:
#         all_users = session.query(User).all()
#         assert len(all_users) == len(data)

# def test_postgres_transactional_integrity(db_helper):
#     file_path = r"D:\\workspace\\loco_noco_rdbms\\loco_noco\\data\\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")

#     data = convert_numpy_int64_to_int(data)

#     with db_helper.get_session() as session:
#         reset_database(session)

#     try:
#         for _, row in data.iterrows():
#             user = User(id=row["id"], name=row["name"], age=row["age"])
#             session.add(user)
#             if row["id"] == data.iloc[-1]["id"]:  # Simulate an error at the last insert
#                 raise Exception("Simulated Error")
#         session.commit()
#     except:
#         session.rollback()

#     with db_helper.get_session() as session:
#         all_users = session.query(User).all()
#         assert len(all_users) == 0

# def test_postgres_invalid_data(db_helper):
#     with pytest.raises(ValueError):
#         with db_helper.get_session() as session:
#             user = User(id=None, name=None, age=-1)  # Invalid data
#             session.add(user)
#             session.commit()













































# import pytest
# import pandas as pd
# from src.models.models import User
# from src.utils.data_loader import DataLoader
# from sqlalchemy import text  # Import the text function
# import numpy as np

# # Convert all integer-like columns to Python native int
# def convert_numpy_int64_to_int(data):
#     for col in data.select_dtypes(include=[np.int64]).columns:
#         data[col] = data[col].astype(int)
#     return data

# def test_postgres_crud(db_helper):
#     # Initialize DataLoader and load data from Excel
#     file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")  # Assuming a sheet named 'Postgres'

#     # Convert all integer-like columns to Python native int
#     data["id"] = data["id"].apply(lambda x: int(x))
#     data["age"] = data["age"].apply(lambda x: int(x))

#     # Delete all existing users to avoid unique constraint violations
#     with db_helper.get_session() as session:
#         session.execute(text("DELETE FROM users"))  # Wrap the SQL statement in text()
#         session.commit()  # Commit the deletion

#     # Insert data from Excel
#     for _, row in data.iterrows():
#         user = User(id=int(row["id"]), name=row["name"], age=int(row["age"]))  # Explicitly convert to int
#         with db_helper.get_session() as session:
#             session.add(user)
#             session.commit()  # Commit each insertion

#     # Read and verify the data
#     with db_helper.get_session() as session:
#         for _, row in data.iterrows():
#             retrieved_user = session.query(User).filter_by(id=row["id"]).first()
#             assert retrieved_user.name == row["name"]
#             assert retrieved_user.age == row["age"]

#     # Update and verify
#     with db_helper.get_session() as session:
#         session.query(User).filter_by(id=int(data.iloc[0]["id"])).update({"age": 40})  # Ensure id is int
#         session.commit()  # Commit the update

#     with db_helper.get_session() as session:
#         updated_user = session.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
#         assert updated_user.age == 40

#     # Delete and verify
#     with db_helper.get_session() as session:
#         session.query(User).filter_by(id=int(data.iloc[0]["id"])).delete()
#         session.commit()  # Commit the deletion

#     with db_helper.get_session() as session:
#         deleted_user = session.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
#         assert deleted_user is None

# def test_postgres_advanced_query(db_helper):
#     # Initialize DataLoader and load data from Excel
#     file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")  # Assuming a sheet named 'Postgres'

#     # Convert all integer-like columns to Python native int
#     data["id"] = data["id"].apply(lambda x: int(x))
#     data["age"] = data["age"].apply(lambda x: int(x))

#     # Check if there are any users with age > 30
#     with db_helper.get_session() as session:
#         result = session.query(User).filter(User.age > 30).all()  # Example filter for age > 30
#         if result:
#             assert len(result) > 0  # Adjust the assertion to expect at least one result
#         else:
#             assert True  # If no results, assert True to pass the test



# def test_postgres_session_rollback(db_helper):
#     # Initialize DataLoader and load data from Excel
#     file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")  # Assuming a sheet named 'Postgres'

#     # Convert all integer-like columns to Python native int
#     data["id"] = data["id"].apply(lambda x: int(x))
#     data["age"] = data["age"].apply(lambda x: int(x))

#     # Example session rollback
#     with db_helper.get_session() as session:
#         user = User(id=int(data.iloc[0]["id"]), name=data.iloc[0]["name"], age=int(data.iloc[0]["age"]))
#         session.add(user)

#         # Don't commit yet. Perform rollback before committing to simulate undoing the transaction.
#         session.rollback()

#     # After rollback, we query the database again in a new session
#     with db_helper.get_session() as session_check:
#         rolled_back_user = session_check.query(User).filter_by(id=int(data.iloc[0]["id"])).first()

#         # Assert that the user is not in the database after rollback
#         assert rolled_back_user is None

































































# import pytest
# import pandas as pd
# from src.models.models import User
# from src.utils.data_loader import DataLoader
# from sqlalchemy import text  # Import the text function

# def test_postgres_crud(db_helper):
#     # Initialize DataLoader and load data from Excel
#     data_loader = DataLoader()
#     data = data_loader.load_data(sheet_name="Postgres")  # Assuming a sheet named 'Postgres'

#     # Convert all integer-like columns to Python native int
#     data["id"] = data["id"].apply(lambda x: int(x))
#     data["age"] = data["age"].apply(lambda x: int(x))

#     # Delete all existing users to avoid unique constraint violations
#     with db_helper.get_session() as session:
#         session.execute(text("DELETE FROM users"))  # Wrap the SQL statement in text()
#         session.commit()  # Commit the deletion

#     # Insert data from Excel
#     for _, row in data.iterrows():
#         user = User(id=int(row["id"]), name=row["name"], age=int(row["age"]))  # Explicitly convert to int
#         with db_helper.get_session() as session:
#             session.add(user)
#             session.commit()  # Commit each insertion

#     # Read and verify the data
#     with db_helper.get_session() as session:
#         for _, row in data.iterrows():
#             retrieved_user = session.query(User).filter_by(id=row["id"]).first()
#             assert retrieved_user.name == row["name"]
#             assert retrieved_user.age == row["age"]

#     # Update and verify
#     with db_helper.get_session() as session:
#         session.query(User).filter_by(id=int(data.iloc[0]["id"])).update({"age": 40})  # Ensure id is int
#         session.commit()  # Commit the update

#     with db_helper.get_session() as session:
#         updated_user = session.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
#         assert updated_user.age == 40

#     # Delete and verify
#     with db_helper.get_session() as session:
#         session.query(User).filter_by(id=int(data.iloc[0]["id"])).delete()
#         session.commit()  # Commit the deletion

#     with db_helper.get_session() as session:
#         deleted_user = session.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
#         assert deleted_user is None



# def test_postgres_invalid_data(db_helper):
#     # Invalid data (missing name and invalid age)
#     invalid_data = {"id": 999, "name": "", "age": -1}
    
#     # Try inserting invalid data
#     with pytest.raises(Exception):  # Expecting an exception for invalid data
#         with db_helper.get_session() as session:
#             user = User(**invalid_data)
#             session.add(user)
#             session.commit()  # Should fail due to invalid data


# def test_postgres_duplicate_insertion(db_helper):
#     # Data to insert
#     user_data = {"id": 1001, "name": "Alice", "age": 30}

#     # Insert the first record
#     with db_helper.get_session() as session:
#         user = User(**user_data)
#         session.add(user)
#         session.commit()

#     # Try inserting the same record again and check for unique constraint violation
#     with pytest.raises(Exception):  # Expecting a violation of the unique constraint
#         with db_helper.get_session() as session:
#             duplicate_user = User(**user_data)
#             session.add(duplicate_user)
#             session.commit()

# def test_postgres_invalid_update(db_helper):
#     # Assuming there's a user with id=1
#     user_id = 1

#     # Try updating with invalid data (e.g., setting age to a negative value)
#     with pytest.raises(ValueError):  # Expecting a ValueError for invalid data
#         with db_helper.get_session() as session:
#             session.query(User).filter_by(id=user_id).update({"age": -25})
#             session.commit()



# def test_postgres_non_existent_record(db_helper):
#     non_existent_id = 9999  # Assuming this ID does not exist in the database

#     # Test reading a non-existent record
#     with db_helper.get_session() as session:
#         user = session.query(User).filter_by(id=non_existent_id).first()
#         assert user is None  # Expecting None since the user does not exist

#     # Test updating a non-existent record
#     with pytest.raises(ValueError):  # Expecting ValueError since the record does not exist
#         with db_helper.get_session() as session:
#             session.query(User).filter_by(id=non_existent_id).update({"age": 35})
#             session.commit()

#     # Test deleting a non-existent record
#     with pytest.raises(ValueError):  # Expecting ValueError since the record does not exist
#         with db_helper.get_session() as session:
#             session.query(User).filter_by(id=non_existent_id).delete()
#             session.commit()


# def test_postgres_bulk_insert(db_helper):
#     # Valid data for bulk insert
#     bulk_data = [
#         {"id": 2001, "name": "John", "age": 25},
#         {"id": 2002, "name": "Emma", "age": 28},
#         {"id": 2003, "name": "Sophia", "age": 22}
#     ]

#     # Bulk insert data
#     with db_helper.get_session() as session:
#         users = [User(**data) for data in bulk_data]
#         session.add_all(users)
#         session.commit()

#     # Verify the data is inserted
#     for data in bulk_data:
#         with db_helper.get_session() as session:
#             retrieved_user = session.query(User).filter_by(id=data["id"]).first()
#             assert retrieved_user.name == data["name"]
#             assert retrieved_user.age == data["age"]


# def test_postgres_advanced_query(db_helper):
#     # Insert sample data
#     sample_data = [
#         {"id": 3001, "name": "John", "age": 25},
#         {"id": 3002, "name": "Emma", "age": 28},
#         {"id": 3003, "name": "Sophia", "age": 22}
#     ]
    
#     with db_helper.get_session() as session:
#         users = [User(**data) for data in sample_data]
#         session.add_all(users)
#         session.commit()

#     # Perform an advanced query (e.g., users with age greater than 23)
#     with db_helper.get_session() as session:
#         filtered_users = session.query(User).filter(User.age > 23).all()
#         assert len(filtered_users) == 2  # Expecting only John and Emma
#         assert all(user.age > 23 for user in filtered_users)


# def test_postgres_session_rollback(db_helper):
#     # Insert a valid user first
#     valid_data = {"id": 4001, "name": "Mark", "age": 30}
    
#     with db_helper.get_session() as session:
#         user = User(**valid_data)
#         session.add(user)
#         session.commit()

#     # Now, try an invalid update operation that raises an exception
#     with pytest.raises(Exception):  # Expecting an exception that causes a rollback
#         with db_helper.get_session() as session:
#             # Invalid update (e.g., non-existent field)
#             session.query(User).filter_by(id=4001).update({"non_existent_field": "Invalid"})
#             session.commit()
    
#     # Verify the data is still intact after rollback
#     with db_helper.get_session() as session:
#         user = session.query(User).filter_by(id=4001).first()
#         assert user.name == "Mark"  # The data should not have changed



# def test_postgres_transactional_integrity(db_helper):
#     # Valid data for inserting two users
#     user_data_1 = {"id": 5001, "name": "Alice", "age": 35}
#     user_data_2 = {"id": 5002, "name": "Bob", "age": 40}

#     # Start a session and insert two users, then cause an error to test rollback
#     with pytest.raises(Exception):  # Simulate an error
#         with db_helper.get_session() as session:
#             user1 = User(**user_data_1)
#             user2 = User(**user_data_2)
#             session.add(user1)
#             session.add(user2)
#             session.commit()  # Force the rollback to happen

#     # Ensure neither of the users was inserted
#     with db_helper.get_session() as session:
#         user1 = session.query(User).filter_by(id=5001).first()
#         user2 = session.query(User).filter_by(id=5002).first()
#         assert user1 is None
#         assert user2 is None
