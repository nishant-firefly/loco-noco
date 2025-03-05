from .base_repo import BaseRepository
from core.models.models import Role
from config.database import DATABASES

class RoleRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    def get_role_by_name(self, name):
        return self.session.query(Role).filter(Role.name == name).first()

    def create_role(self, role_data):
        return self.create(Role, role_data)


    def update_role(self, role_id: int, update_data: dict):
        role = self.session.get(Role, role_id)
        if not role:
            return None  # Role not found

        for key, value in update_data.items():
            setattr(role, key, value)

        self.session.commit()
        self.session.refresh(role)
        return role

    def delete_role(self, role_id: int):
        role = self.session.get(Role, role_id)
        if not role:
            return False  # Role not found

        self.session.delete(role)
        self.session.commit()
        return True