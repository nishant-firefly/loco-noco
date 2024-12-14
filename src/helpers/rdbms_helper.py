from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from src.models.models import User  # Assuming the User model is imported from models

class RDBMSHelper:
    def __init__(self, db_url):
        """
        Initialize the RDBMS helper with a database URL.
        :param db_url: Database connection string
        """
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self):
        """
        Provide a database session for operations.
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def create_all_tables(self, base):
        """
        Create all tables defined in the SQLAlchemy Base.
        :param base: SQLAlchemy declarative Base object
        """
        base.metadata.create_all(self.engine)

    def drop_all_tables(self, base):
        """
        Drop all tables defined in the SQLAlchemy Base.
        :param base: SQLAlchemy declarative Base object
        """
        base.metadata.drop_all(self.engine)

    # CRUD Operations

    def create_user(self, user_data):
        """Create a new user."""
        with self.get_session() as session:
            try:
                user = User(**user_data)
                session.add(user)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise ValueError("Error creating user: Integrity Error") from e
            except Exception as e:
                session.rollback()
                raise ValueError("Error creating user") from e

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        with self.get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            return user

    def update_user(self, user_id, updated_data):
        """Update an existing user."""
        with self.get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            for key, value in updated_data.items():
                setattr(user, key, value)

            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise ValueError("Error updating user: Integrity Error") from e
            except Exception as e:
                session.rollback()
                raise ValueError("Error updating user") from e

    def delete_user(self, user_id):
        """Delete a user by ID."""
        with self.get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            session.delete(user)
            session.commit()

    def get_all_users(self):
        """Retrieve all users."""
        with self.get_session() as session:
            users = session.query(User).all()
            return users











# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from contextlib import contextmanager
# import pandas as pd


# class RDBMSHelper:
#     def __init__(self, db_url):
#         self.engine = create_engine(db_url)
#         self.Session = sessionmaker(bind=self.engine)

#     @contextmanager
#     def get_session(self):
#         session = self.Session()
#         try:
#             yield session
#             session.commit()
#         except Exception as e:
#             session.rollback()
#             raise
#         finally:
#             session.close()

#     def create_all_tables(self, base):
#         """
#         Create all tables in the database based on the SQLAlchemy Base.
#         :param base: SQLAlchemy Base containing table definitions
#         """
#         base.metadata.create_all(self.engine)

#     def drop_all_tables(self, base):
#         """
#         Drop all tables in the database based on the SQLAlchemy Base.
#         :param base: SQLAlchemy Base containing table definitions
#         """
#         try:
#             base.metadata.drop_all(self.engine)
#         except Exception as e:
#             print(f"Error during table drop: {e}")
#             raise RuntimeError("Failed to drop tables.") 
#     def create_bulk_from_excel(self, model, file_path, sheet_name):
#         """
#         Bulk insert records into the database from an Excel sheet.
#         """
#         with self.get_session() as session:
#             data = pd.read_excel(file_path, sheet_name=sheet_name)
#             records = [model(**row.to_dict()) for _, row in data.iterrows()]
#             session.add_all(records)
#             session.commit()










# # General RDBMS helper (SQLAlchemy-based)
# from contextlib import contextmanager
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine

# class RDBMSHelper:
#     def __init__(self, db_url):
#         """
#         Initialize the RDBMS helper with a database URL.
#         :param db_url: Database connection string
#         """
#         self.engine = create_engine(db_url)
#         self.Session = sessionmaker(bind=self.engine)

#     @contextmanager
#     def get_session(self):
#         """
#         Provide a database session for operations.
#         """
#         session = self.Session()
#         try:
#             yield session
#             session.commit()
#         except Exception as e:
#             session.rollback()
#             raise
#         finally:
#             session.close()

#     def create_all_tables(self, base):
#         """
#         Create all tables defined in the SQLAlchemy Base.
#         :param base: SQLAlchemy declarative Base object
#         """
#         base.metadata.create_all(self.engine)

#     def drop_all_tables(self, base):
#         """
#         Drop all tables defined in the SQLAlchemy Base.
#         :param base: SQLAlchemy declarative Base object
#         """
#         base.metadata.drop_all(self.engine)
