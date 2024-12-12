import pytest
import pandas as pd
from src.models.models import User
from src.utils.data_loader import DataLoader
from sqlalchemy import text  # Import the text function

def test_postgres_crud(db_helper):
    # Initialize DataLoader and load data from Excel
    data_loader = DataLoader()
    data = data_loader.load_data(sheet_name="Postgres")  # Assuming a sheet named 'Postgres'

    # Convert all integer-like columns to Python native int
    data["id"] = data["id"].apply(lambda x: int(x))
    data["age"] = data["age"].apply(lambda x: int(x))

    # Delete all existing users to avoid unique constraint violations
    with db_helper.get_session() as session:
        session.execute(text("DELETE FROM users"))  # Wrap the SQL statement in text()
        session.commit()  # Commit the deletion

    # Insert data from Excel
    for _, row in data.iterrows():
        user = User(id=int(row["id"]), name=row["name"], age=int(row["age"]))  # Explicitly convert to int
        with db_helper.get_session() as session:
            session.add(user)
            session.commit()  # Commit each insertion

    # Read and verify the data
    with db_helper.get_session() as session:
        for _, row in data.iterrows():
            retrieved_user = session.query(User).filter_by(id=row["id"]).first()
            assert retrieved_user.name == row["name"]
            assert retrieved_user.age == row["age"]

    # Update and verify
    with db_helper.get_session() as session:
        session.query(User).filter_by(id=int(data.iloc[0]["id"])).update({"age": 40})  # Ensure id is int
        session.commit()  # Commit the update

    with db_helper.get_session() as session:
        updated_user = session.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
        assert updated_user.age == 40

    # Delete and verify
    with db_helper.get_session() as session:
        session.query(User).filter_by(id=int(data.iloc[0]["id"])).delete()
        session.commit()  # Commit the deletion

    with db_helper.get_session() as session:
        deleted_user = session.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
        assert deleted_user is None











# import pytest
# import pandas as pd
# from src.models.models import User
# from src.utils.data_loader import DataLoader



# def test_postgres_crud(db_helper):
#     # Initialize DataLoader and load data from Excel
#     data_loader = DataLoader()
#     data = data_loader.load_data(sheet_name="Postgres")  # Assuming a sheet named 'Postgres'

#     # Convert all integer-like columns to Python native int
#     data["id"] = data["id"].apply(lambda x: int(x))
#     data["age"] = data["age"].apply(lambda x: int(x))

#     # Insert data from Excel
#     for _, row in data.iterrows():
#         user = User(id=int(row["id"]), name=row["name"], age=int(row["age"]))  # Explicitly convert to int
#         with db_helper.get_session() as session:
#             session.add(user)

#     # Read and verify the data
#     with db_helper.get_session() as session:
#         for _, row in data.iterrows():
#             retrieved_user = session.query(User).filter_by(id=row["id"]).first()
#             assert retrieved_user.name == row["name"]
#             assert retrieved_user.age == row["age"]

#     # Update and verify
#     with db_helper.get_session() as session:
#         session.query(User).filter_by(id=int(data.iloc[0]["id"])).update({"age": 40})  # Ensure id is int

#     with db_helper.get_session() as session:
#         updated_user = session.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
#         assert updated_user.age == 40

#     # Delete and verify
#     with db_helper.get_session() as session:
#         session.query(User).filter_by(id=int(data.iloc[0]["id"])).delete()

#     with db_helper.get_session() as session:
#         deleted_user = session.query(User).filter_by(id=int(data.iloc[0]["id"])).first()
#         assert deleted_user is None









