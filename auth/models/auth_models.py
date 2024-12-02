# Models for the Auth Module
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, JSON, TIMESTAMP
from sqlalchemy.orm import relationship
from sources.rdbms.models.models import Base

class Grouping(Base):
    __tablename__ = "grouping"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("grouping.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Self-referencing relationship
    children = relationship("Grouping", backref="parent", remote_side=[id])

class UserGrouping(Base):
    __tablename__ = "user_grouping"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    grouping_id = Column(Integer, ForeignKey("grouping.id", ondelete="CASCADE"), nullable=False)

class Entity(Base):
    __tablename__ = "entity"

    id = Column(Integer, primary_key=True)
    source = Column(Enum("postgres", "elasticsearch", "aws_s3"), nullable=False)
    name = Column(String, nullable=False)

class Permissions(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    grouping_id = Column(Integer, ForeignKey("grouping.id", ondelete="CASCADE"), nullable=False)
    entity_id = Column(Integer, ForeignKey("entity.id", ondelete="CASCADE"), nullable=False)
    permission_json = Column(JSON, nullable=False)
