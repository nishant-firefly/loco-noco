
import sys
import os

# Dynamically set the root directory (multi_db_query_builder) as the module path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from core.models.models import User, Role, EntityRolePermission, RoleToUserMapping
from core.models.base import Base
from config.database import DATABASES
from typing import Dict, Any, List



# Set the root directory (multi_db_query_builder) as the module path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class QueryBuilder:
    def __init__(self, db_type: str):
        """Initialize QueryBuilder with the selected database"""
        if db_type not in DATABASES:
            raise ValueError(f"Unsupported database type: {db_type}")
        
        self.engine = create_engine(DATABASES[db_type])
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def execute_query(self, query: str, params: Dict[str, Any] = None):
        """Execute a raw SQL query with optional parameters."""
        session = self.SessionLocal()
        try:
            result = session.execute(text(query), params or {})
            session.commit()
            return result.fetchall()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def select(self, model, columns: List[str] = None, filters: Dict[str, Any] = None):
        """Generate a SELECT query using model references."""
        table_name = model.__tablename__
        selected_columns = ", ".join(columns) if columns else "*"
        query = f"SELECT {selected_columns} FROM {table_name}"
        
        if filters:
            where_clauses = [f"{col} = :{col}" for col in filters.keys()]
            query += f" WHERE {' AND '.join(where_clauses)}"
        
        return self.execute_query(query, filters)

    def insert(self, model, data: Dict[str, Any]):
        """Generate an INSERT query dynamically."""
        table_name = model.__tablename__
        columns = ", ".join(data.keys())
        values = ", ".join([f":{col}" for col in data.keys()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) RETURNING *"
        return self.execute_query(query, data)

    def update(self, model, data: Dict[str, Any], filters: Dict[str, Any]):
        """Generate an UPDATE query dynamically."""
        table_name = model.__tablename__
        set_clause = ", ".join([f"{col} = :{col}" for col in data.keys()])
        where_clause = " AND ".join([f"{col} = :where_{col}" for col in filters.keys()])
        
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause} RETURNING *"
        
        params = {**data, **{f"where_{k}": v for k, v in filters.items()}}
        return self.execute_query(query, params)

    def delete(self, model, filters: Dict[str, Any]):
        """Generate a DELETE query dynamically."""
        table_name = model.__tablename__
        where_clause = " AND ".join([f"{col} = :{col}" for col in filters.keys()])
        query = f"DELETE FROM {table_name} WHERE {where_clause} RETURNING *"
        return self.execute_query(query, filters)

    def apply_authorization(self, query: str, user_role: str):
        """Modify query based on user role and permissions."""
        if user_role == "admin":
            return query  # Admin has full access
        elif user_role == "user":
            return query + " WHERE is_private = FALSE"  # Restrict access to private data
        else:
            return query + " WHERE access_level = 'public'"

    def apply_column_restrictions(self, query: str, user_role: str, allowed_columns: List[str]):
        """Limit query results to authorized columns only."""
        if user_role != "admin":
            query = query.replace("*", ", ".join(allowed_columns))
        return query


if __name__ == "__main__":
    qb = QueryBuilder("postgres")

    # Insert Example (Include `username` to avoid NOT NULL error)
    print(qb.insert(User, {
        "first_name": "John", 
        "last_name": "Doe", 
        "username": "johndoe",  # <-- Add this field
        "email": "john@example.com",
        "password": "securepassword123"  # <-- Add password as it's NOT NULL too
    }))



    # Select Example (Corrected to use User model)
    print(qb.select(User, ["id", "first_name"], {"email": "john@example.com"}))

    # Update Example (Corrected to use User model)
    print(qb.update(User, {"first_name": "Johnny"}, {"email": "john@example.com"}))

    # Delete Example (Corrected to use User model)
    print(qb.delete(User, {"email": "john@example.com"}))
