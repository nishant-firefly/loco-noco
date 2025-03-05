from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_session
from config.database import DATABASES
from core.repositories.role_to_user_repo import RoleToUserRepository
from pydantic import BaseModel
from core.models.models import User, Role, EntityRolePermission, RoleToUserMapping
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

class AssignRoleRequest(BaseModel):
    user_id: int
    role_id: int

class UnassignRoleRequest(BaseModel):
    user_id: int
    role_id: int





@router.post("/roles/assign")
def assign_role(data: AssignRoleRequest, session: Session = Depends(get_session)):
    role_to_user_repo = RoleToUserRepository(session)
    assigned_role = role_to_user_repo.assign_role_to_user(data.user_id, data.role_id)
    return assigned_role

@router.get("/users/{user_id}/roles")
def get_user_roles(user_id: int, session: Session = Depends(get_session)):
    role_to_user_repo = RoleToUserRepository(session)
    roles = role_to_user_repo.get_roles_for_user(user_id)
    return roles

@router.delete("/roles/unassign")
def unassign_role(data: UnassignRoleRequest, session: Session = Depends(get_session)):
    role_to_user_repo = RoleToUserRepository(session)
    return {"message": "Role unassigned successfully"} if role_to_user_repo.unassign_role_from_user(data.user_id, data.role_id) else {"error": "Role or User not found"}



@router.get("/roles/{role_id}/users")
def get_users_by_role(role_id: int, session: Session = Depends(get_session)):
    role_to_user_repo = RoleToUserRepository(session)
    return role_to_user_repo.get_users_for_role(role_id)