from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.models.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    joined_on = Column(DateTime, default=datetime.utcnow)
    
    roles = relationship("RoleToUserMapping", back_populates="user")



class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("RoleToUserMapping", back_populates="role")
    permissions = relationship("EntityRolePermission", back_populates="role")  # Add this line

# class Role(Base):
#     __tablename__ = "roles"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, nullable=False)

#     users = relationship("RoleToUserMapping", back_populates="role")


class EntityRolePermission(Base):
    __tablename__ = "entity_role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    entity_id = Column(Integer, nullable=False)
    create = Column(Boolean, default=False)
    read = Column(Boolean, default=True)
    update = Column(Boolean, default=False)
    delete = Column(Boolean, default=False)

    role = relationship("Role", back_populates="permissions")


class RoleToUserMapping(Base):
    __tablename__ = "role_to_user_mapping"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    refresh_config = Column(Boolean, default=False)

    role = relationship("Role", back_populates="users")
    user = relationship("User", back_populates="roles")
