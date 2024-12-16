import pytest
import pandas as pd
from unittest.mock import MagicMock
from sqlalchemy import text
from src.models.models import User, Product, Order
from src.utils.data_loader import DataLoader
from src.services.user_service import UserService  # Assuming this is the location of your service layer
from sqlalchemy.exc import IntegrityError


# Reusable fixture for db_helper
@pytest.fixture
def mock_db_helper():
    mock_db_helper = MagicMock()
    mock_session = MagicMock()
    mock_db_helper.get_session.return_value.__enter__.return_value = mock_session
    return mock_db_helper

# Load data from Excel
@pytest.fixture
def load_test_data():
    file_path = r"D:\\workspace\\loco_noco_rdbms\\test_multiple_data.xlsx"
    data_loader = DataLoader(file_path=file_path)
    users_data = data_loader.load_data(sheet_name="users").to_dict(orient="records")
    products_data = data_loader.load_data(sheet_name="products").to_dict(orient="records")
    orders_data = data_loader.load_data(sheet_name="orders").to_dict(orient="records")
    return users_data, products_data, orders_data

# Service Layer Test: Create Single User
def test_user_service_create_user(mock_db_helper, load_test_data):
    user_service = UserService(db_helper=mock_db_helper)
    users_data, _, _ = load_test_data

    # Test creating a user
    user_service.create_user(users_data[0])

    # Validate
    mock_db_helper.get_session.assert_called_once()  # Ensure session was opened
    mock_session = mock_db_helper.get_session.return_value.__enter__.return_value
    mock_session.add.assert_called_once()  # Ensure user was added to the session
    mock_session.commit.assert_called_once()  # Ensure session was committed

# Service Layer Test: Bulk Create Users
def test_user_service_bulk_create(mock_db_helper, load_test_data):
    user_service = UserService(db_helper=mock_db_helper)
    users_data, _, _ = load_test_data

    # Test bulk creation of users
    user_service.create_bulk_users(users_data)

    # Validate
    mock_session = mock_db_helper.get_session.return_value.__enter__.return_value
    mock_session.bulk_save_objects.assert_called_once()  # Bulk save should be called once
    mock_session.commit.assert_called_once()  # Ensure session was committed

# Service Layer Test: Retrieve User
def test_user_service_get_user(mock_db_helper):
    # Mock the session behavior
    mock_session = mock_db_helper.get_session.return_value.__enter__.return_value
    mock_user = User(id=1, name="John Doe", age=30)
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user

    user_service = UserService(db_helper=mock_db_helper)
    user = user_service.get_user(1)

    # Validate
    mock_session.query.assert_called_once()  # Ensure query was called
    assert user.id == 1
    assert user.name == "John Doe"
    assert user.age == 30

# Integration Test for CRUD Operations with Data
def test_integration_crud_operations(db_helper, load_test_data):
    users_data, products_data, orders_data = load_test_data

    # Clear tables
    with db_helper.get_session() as session:
        session.execute(text("DELETE FROM orders"))
        session.execute(text("DELETE FROM products"))
        session.execute(text("DELETE FROM users"))
        session.commit()

    # Insert Users
    user_service = UserService(db_helper)
    user_service.create_bulk_users(users_data)

    # Verify Users
    with db_helper.get_session() as session:
        assert session.query(User).count() == len(users_data)

    # Insert Products
    products = [Product(**product) for product in products_data]
    with db_helper.get_session() as session:
        session.bulk_save_objects(products)
        session.commit()

    # Verify Products
    with db_helper.get_session() as session:
        assert session.query(Product).count() == len(products_data)

    # Insert Orders
    orders = [Order(**order) for order in orders_data]
    with db_helper.get_session() as session:
        session.bulk_save_objects(orders)
        session.commit()

    # Verify Orders
    with db_helper.get_session() as session:
        assert session.query(Order).count() == len(orders_data)

# Error Handling Test: IntegrityError
def test_user_service_integrity_error(mock_db_helper, load_test_data):
    user_service = UserService(db_helper=mock_db_helper)
    users_data, _, _ = load_test_data

    # Mock IntegrityError
    mock_session = mock_db_helper.get_session.return_value.__enter__.return_value
    mock_session.commit.side_effect = IntegrityError("Integrity constraint violated", None, None)

    with pytest.raises(IntegrityError):
        user_service.create_user(users_data[0])  # Try creating a user

    # Ensure rollback was called
    mock_session.rollback.assert_called_once()
























































# import pytest
# import pandas as pd
# from unittest.mock import MagicMock
# from src.models.models import User, Product, Order
# from src.utils.data_loader import DataLoader
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import text

# # Service Layer (DDD)
# class UserService:
#     def __init__(self, db_helper):
#         self.db_helper = db_helper

#     def create_user(self, user_data):
#         user = User(**user_data)
#         with self.db_helper.get_session() as session:
#             session.add(user)
#             session.commit()

#     def get_user(self, user_id):
#         with self.db_helper.get_session() as session:
#             return session.query(User).filter_by(id=user_id).first()

#     def create_bulk_users(self, users_data):
#         users = [User(**user) for user in users_data]
#         with self.db_helper.get_session() as session:
#             session.bulk_save_objects(users)
#             session.commit()

# # Test for UserService
# def test_user_service_create_user():
#     # Mock db_helper and session
#     mock_db_helper = MagicMock()
#     mock_session = MagicMock()
#     mock_db_helper.get_session.return_value.__enter__.return_value = mock_session

#     user_service = UserService(db_helper=mock_db_helper)

#     # Input data from Excel
#     file_path = r"D:\\workspace\\loco_noco_rdbms\\test_multiple_data.xlsx"
#     users_data = pd.read_excel(file_path, sheet_name="users").to_dict(orient="records")

#     # Test creating a user
#     user_service.create_user(users_data[0])

#     mock_session.add.assert_called_once()  # Ensure the user was added to the session
#     mock_session.commit.assert_called_once()  # Ensure the session was committed

# def test_user_service_bulk_create():
#     # Mock db_helper and session
#     mock_db_helper = MagicMock()
#     mock_session = MagicMock()
#     mock_db_helper.get_session.return_value.__enter__.return_value = mock_session

#     user_service = UserService(db_helper=mock_db_helper)

#     # Input data from Excel
#     file_path = r"D:\\workspace\\loco_noco_rdbms\\test_multiple_data.xlsx"
#     users_data = pd.read_excel(file_path, sheet_name="users").to_dict(orient="records")

#     # Test bulk creation of users
#     user_service.create_bulk_users(users_data)

#     assert mock_session.bulk_save_objects.call_count == 1  # Bulk save should be called once
#     mock_session.commit.assert_called_once()  # Ensure the session was committed

# def test_user_service_get_user():
#     # Mock db_helper and session
#     mock_db_helper = MagicMock()
#     mock_session = MagicMock()
#     mock_db_helper.get_session.return_value.__enter__.return_value = mock_session

#     # Mock the return value of query
#     mock_user = User(id=1, name="John Doe", age=30)
#     mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user

#     user_service = UserService(db_helper=mock_db_helper)

#     # Test retrieving a user
#     user = user_service.get_user(1)

#     mock_session.query.assert_called_once()  # Ensure query was called
#     assert user.id == 1
#     assert user.name == "John Doe"
#     assert user.age == 30

# # Integration Test for CRUD operations with data from Excel
# def test_integration_crud_operations(db_helper):
#     # DataLoader to read Excel file
#     file_path = r"D:\\workspace\\loco_noco_rdbms\\test_multiple_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)

#     users_data = data_loader.load_data(sheet_name="users")
#     products_data = data_loader.load_data(sheet_name="products")
#     orders_data = data_loader.load_data(sheet_name="orders")

#     # Convert data to dictionaries
#     users_data = users_data.to_dict(orient="records")
#     products_data = products_data.to_dict(orient="records")
#     orders_data = orders_data.to_dict(orient="records")

#     # Clear tables
#     with db_helper.get_session() as session:
#         session.execute(text("DELETE FROM orders"))  # Wrap raw SQL in text()
#         session.execute(text("DELETE FROM products"))  # Wrap raw SQL in text()
#         session.execute(text("DELETE FROM users"))  # Wrap raw SQL in text()
#         session.commit()

#     # Insert Users
#     user_service = UserService(db_helper)
#     user_service.create_bulk_users(users_data)

#     # Verify Users
#     with db_helper.get_session() as session:
#         assert session.query(User).count() == len(users_data)

#     # Insert Products
#     products = [Product(**product) for product in products_data]
#     with db_helper.get_session() as session:
#         session.bulk_save_objects(products)
#         session.commit()

#     # Verify Products
#     with db_helper.get_session() as session:
#         assert session.query(Product).count() == len(products_data)

#     # Insert Orders
#     orders = [Order(**order) for order in orders_data]
#     with db_helper.get_session() as session:
#         session.bulk_save_objects(orders)
#         session.commit()

#     # Verify Orders
#     with db_helper.get_session() as session:
#         assert session.query(Order).count() == len(orders_data)



































# import pytest
# import pandas as pd
# from src.models.models import User
# from src.utils.data_loader import DataLoader
# from sqlalchemy import text  # Import the text function
# import numpy as np
# import sqlalchemy


# # Convert all integer-like columns to Python native int
# def convert_numpy_int64_to_int(data):
#     for col in data.select_dtypes(include=[np.int64]).columns:
#         data[col] = data[col].astype(int)
#     return data

# # Test for basic CRUD operations
# def test_postgres_crud(db_helper):
#     file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")
#     data["id"] = data["id"].apply(lambda x: int(x))
#     data["age"] = data["age"].apply(lambda x: int(x))

#     with db_helper.get_session() as session:
#         session.execute(text("DELETE FROM users"))
#         session.commit()

#     for _, row in data.iterrows():
#         user = User(id=int(row["id"]), name=row["name"], age=int(row["age"]))
#         with db_helper.get_session() as session:
#             session.add(user)
#             session.commit()

#     with db_helper.get_session() as session:
#         for _, row in data.iterrows():
#             retrieved_user = session.query(User).filter_by(id=row["id"]).first()
#             assert retrieved_user.name == row["name"]
#             assert retrieved_user.age == row["age"]

#     with db_helper.get_session() as session:
#         session.query(User).filter_by(id=int(data.iloc[0]["id"])).update({"age": 40})
#         session.commit()

#     with db_helper.get_session() as session:
#         updated_user = session.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
#         assert updated_user.age == 40

#     with db_helper.get_session() as session:
#         session.query(User).filter_by(id=int(data.iloc[0]["id"])).delete()
#         session.commit()

#     with db_helper.get_session() as session:
#         deleted_user = session.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
#         assert deleted_user is None

# # Test for advanced query filters
# def test_postgres_advanced_query(db_helper):
#     file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")
#     data["id"] = data["id"].apply(lambda x: int(x))
#     data["age"] = data["age"].apply(lambda x: int(x))

#     with db_helper.get_session() as session:
#         result = session.query(User).filter(User.age > 30).all()
#         assert len(result) > 0 if result else True

# # Test for session rollback functionality
# def test_postgres_session_rollback(db_helper):
#     file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")
#     data["id"] = data["id"].apply(lambda x: int(x))
#     data["age"] = data["age"].apply(lambda x: int(x))

#     with db_helper.get_session() as session:
#         user = User(id=int(data.iloc[0]["id"]), name=data.iloc[0]["name"], age=int(data.iloc[0]["age"]))
#         session.add(user)
#         session.rollback()

#     with db_helper.get_session() as session_check:
#         rolled_back_user = session_check.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
#         assert rolled_back_user is None

# # Test for invalid data handling
# def test_postgres_invalid_data(db_helper):
#     with db_helper.get_session() as session:
#         try:
#             invalid_user = User(id="abc", name=None, age=-10)
#             session.add(invalid_user)
#             session.commit()
#         except Exception as e:
#             session.rollback()
#             assert isinstance(e, (ValueError, sqlalchemy.exc.SQLAlchemyError))

# # Test for transactional integrity
# def test_postgres_transactional_integrity(db_helper):
#     with db_helper.get_session() as session:
#         try:
#             valid_user = User(id=1, name="John Doe", age=30)
#             session.add(valid_user)

#             invalid_user = User(id="abc", name=None, age=-10)
#             session.add(invalid_user)

#             session.commit()
#         except Exception:
#             session.rollback()

#     with db_helper.get_session() as session_check:
#         result = session_check.query(User).filter_by(id=1).first()
#         assert result is None

# # Test for bulk insert
# def test_postgres_bulk_insert(db_helper):
#     # Clear the users table
#     with db_helper.get_session() as session:
#         session.execute(text("DELETE FROM users"))
#         session.commit()

#     # Load test data
#     file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")

#     # Convert numpy.int64 to int
#     data["id"] = data["id"].apply(lambda x: int(x))
#     data["age"] = data["age"].apply(lambda x: int(x))

#     # Bulk insert
#     users = [User(id=int(row["id"]), name=row["name"], age=int(row["age"])) for _, row in data.iterrows()]
#     with db_helper.get_session() as session:
#         session.bulk_save_objects(users)
#         session.commit()

#     # Verify the inserted data
#     with db_helper.get_session() as session:
#         for _, row in data.iterrows():
#             retrieved_user = session.query(User).filter_by(id=int(row["id"])).first()
#             assert retrieved_user is not None
#             assert retrieved_user.name == row["name"]
#             assert retrieved_user.age == int(row["age"])


# # Test for duplicate insertion
# def test_postgres_duplicate_insertion(db_helper):
#     # Clear the users table
#     with db_helper.get_session() as session:
#         session.execute(text("DELETE FROM users"))
#         session.commit()

#     # Load test data
#     file_path = r"D:\workspace\loco_noco_rdbms\loco_noco\data\test_data.xlsx"
#     data_loader = DataLoader(file_path=file_path)
#     data = data_loader.load_data(sheet_name="Postgres")

#     # Convert numpy.int64 to int
#     data["id"] = data["id"].apply(lambda x: int(x))
#     data["age"] = data["age"].apply(lambda x: int(x))

#     # Insert a single record
#     user = User(id=int(data.iloc[0]["id"]), name=data.iloc[0]["name"], age=int(data.iloc[0]["age"]))
#     with db_helper.get_session() as session:
#         session.add(user)
#         session.commit()

#     # Attempt to insert the same record again, expecting a unique constraint violation
#     with db_helper.get_session() as session:
#         duplicate_user = User(id=int(data.iloc[0]["id"]), name=data.iloc[0]["name"], age=int(data.iloc[0]["age"]))
#         try:
#             session.add(duplicate_user)
#             session.commit()
#         except Exception as exc:
#             session.rollback()  # Explicitly roll back the session after the exception
#             assert "duplicate key value" in str(exc)

#     # Verify that no additional record was inserted
#     with db_helper.get_session() as session:
#         count = session.query(User).filter_by(id=int(data.iloc[0]["id"])).count()
#         assert count == 1


































