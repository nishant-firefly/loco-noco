from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_session
from config.database import DATABASES
from core.repositories.role_repo import RoleRepository
from pydantic import BaseModel
from core.models.models import User, Role, EntityRolePermission, RoleToUserMapping
router = APIRouter()

class RoleCreate(BaseModel):
    name: str


class RoleUpdate(BaseModel):
    name: str | None = None


@router.post("/roles/")
def create_role(role_data: RoleCreate, session: Session = Depends(get_session)):
    role_repo = RoleRepository(session)
    existing_role = role_repo.get_role_by_name(role_data.name)
    if existing_role:
        return {"error": "Role already exists"}
    
    new_role = role_repo.create_role(role_data.dict())
    return new_role

@router.get("/roles/{role_id}")
def get_role(role_id: int, session: Session = Depends(get_session)):
    role_repo = RoleRepository(session)
    role = role_repo.get(Role, role_id)
    if not role:
        return {"error": "Role not found"}
    return role


@router.put("/roles/{role_id}")
def update_role(role_id: int, role_data: RoleUpdate, session: Session = Depends(get_session)):
    role_repo = RoleRepository(session)
    updated_role = role_repo.update_role(role_id, role_data.dict(exclude_unset=True))
    return updated_role if updated_role else {"error": "Role not found"}

@router.delete("/roles/{role_id}")
def delete_role(role_id: int, session: Session = Depends(get_session)):
    role_repo = RoleRepository(session)
    return {"message": "Role deleted successfully"} if role_repo.delete_role(role_id) else {"error": "Role not found"}