from .base_repo import BaseRepository
from core.models.models import RoleToUserMapping,User,Role
from config.database import DATABASES

class RoleToUserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    def assign_role_to_user(self, user_id, role_id):
        role_mapping = RoleToUserMapping(user_id=user_id, role_id=role_id)
        self.session.add(role_mapping)
        self.session.commit()
        self.session.refresh(role_mapping)
        return role_mapping

    def get_roles_for_user(self, user_id):
        return self.session.query(RoleToUserMapping).filter(RoleToUserMapping.user_id == user_id).all()


    def get_users_for_role(self, role_id: int):
        return self.session.query(User).join(RoleToUserMapping).filter(RoleToUserMapping.role_id == role_id).all()

    
    def delete_role_from_user(self, user_id: int, role_id: int):
        role_mapping = (
            self.session.query(RoleToUserMapping)
            .filter_by(user_id=user_id, role_id=role_id)
            .first()
        )
        
        if not role_mapping:
            return None  # Or raise an exception if needed
        
        self.session.delete(role_mapping)
        self.session.commit()
        return {"message": "Role unassigned successfully"}