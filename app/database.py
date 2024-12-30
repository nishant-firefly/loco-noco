from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import time
from app.config.test_config import TEST_ENV_CONFIG
import psycopg2



# Read database credentials from test_config.py
db_config = TEST_ENV_CONFIG["services"]["postgres"]["environment"]
DATABASE_URL = f"postgresql://{db_config['POSTGRES_USER']}:{db_config['POSTGRES_PASSWORD']}@localhost:{5432}/{db_config['POSTGRES_DB']}"

# Create the engine and session maker
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to check PostgreSQL service health
def wait_for_postgres():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=db_config["POSTGRES_DB"],
                user=db_config["POSTGRES_USER"],
                password=db_config["POSTGRES_PASSWORD"],
                host="localhost",
                port=5432
            )
            conn.close()
            break
        except psycopg2.OperationalError:
            print("PostgreSQL is not ready. Retrying...")
            time.sleep(5)

# Wait for PostgreSQL to be ready before running tests
wait_for_postgres()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to execute a raw SQL query
def execute_query(sql_query, params=None, fetch_all=True):
    """
    Execute a raw SQL query using the database engine.

    Args:
        sql_query (str): The SQL query to execute.
        params (dict): Optional dictionary of query parameters.
        fetch_all (bool): Whether to fetch all results or just one.

    Returns:
        list or dict: Query results for SELECT queries or success message for others.
    """
    with engine.connect() as connection:
        try:
            result = connection.execute(text(sql_query), params or {})
            if result.returns_rows:
                if fetch_all:
                    return result.fetchall()  # Return all rows
                else:
                    return result.fetchone()  # Return one row
            else:
                return {"message": "Query executed successfully"}
        except Exception as e:
            print(f"Error executing query: {e}")
            return {"error": str(e)}
        


# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# import os
# import time
# from app.config.test_config import TEST_ENV_CONFIG
# import psycopg2

# # Read database credentials from test_config.py
# db_config = TEST_ENV_CONFIG["services"]["postgres"]["environment"]
# DATABASE_URL = f"postgresql://{db_config['POSTGRES_USER']}:{db_config['POSTGRES_PASSWORD']}@localhost:{5432}/{db_config['POSTGRES_DB']}"

# # Create the engine and session maker
# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# class Database:
#     def __init__(self):
#         self.engine = engine

#     def execute_query(self, sql_query, params=None, fetch_all=True):
#         """
#         Execute a raw SQL query using the database engine.

#         Args:
#             sql_query (str): The SQL query to execute.
#             params (dict): Optional dictionary of query parameters.
#             fetch_all (bool): Whether to fetch all results or just one.

#         Returns:
#             list or dict: Query results for SELECT queries or success message for others.
#         """
#         with self.engine.connect() as connection:
#             try:
#                 result = connection.execute(text(sql_query), params or {})
#                 if result.returns_rows:
#                     if fetch_all:
#                         return result.fetchall()  # Return all rows
#                     else:
#                         return result.fetchone()  # Return one row
#                 else:
#                     return {"message": "Query executed successfully"}
#             except Exception as e:
#                 print(f"Error executing query: {e}")
#                 return {"error": str(e)}

#     @staticmethod
#     def wait_for_postgres():
#         while True:
#             try:
#                 conn = psycopg2.connect(
#                     dbname=db_config["POSTGRES_DB"],
#                     user=db_config["POSTGRES_USER"],
#                     password=db_config["POSTGRES_PASSWORD"],
#                     host="localhost",
#                     port=5432
#                 )
#                 conn.close()
#                 break
#             except psycopg2.OperationalError:
#                 print("PostgreSQL is not ready. Retrying...")
#                 time.sleep(5)

#     @staticmethod
#     def get_db():
#         db = SessionLocal()
#         try:
#             yield db
#         finally:
#             db.close()

# # Wait for PostgreSQL to be ready
# Database.wait_for_postgres()