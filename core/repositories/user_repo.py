from .base_repo import BaseRepository
from core.models.models import User
from config.database import DATABASES

class UserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    def get_user_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def create_user(self, user_data):
        return self.create(User, user_data)


    def update_user(self, user_id: int, update_data: dict):
        user = self.session.get(User, user_id)
        if not user:
            return None  # Or raise an exception

        for key, value in update_data.items():
            setattr(user, key, value)

        self.session.commit()
        self.session.refresh(user)
        return user



    def delete_user(self, user_id: int) -> bool:
        user = self.session.get(User, user_id)
        if not user:
            return False  # User not found

        self.session.delete(user)
        self.session.commit()
        return True


