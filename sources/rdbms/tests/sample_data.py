from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, JSON

Base = declarative_base()

# Sample User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

# Sample Permission model
class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    entity_type = Column(Enum("table", "bucket", "index"), nullable=False)
    entity_name = Column(String, nullable=False)
    permission_json = Column(JSON, nullable=False)

# Helper function to populate sample data
def populate_sample_data(session):
    # Add sample users
    session.add_all([
        User(name="John Doe", email="john.doe@example.com"),
        User(name="Jane Smith", email="jane.smith@example.com")
    ])

    # Add sample permissions
    session.add(
        Permission(
            entity_type="table",
            entity_name="users",
            permission_json={
                "create": True,
                "read": True,
                "update": False,
                "delete": False
            }
        )
    )

    session.commit()