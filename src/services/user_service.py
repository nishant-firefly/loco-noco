from src.models.models import User
from sqlalchemy.exc import IntegrityError




class UserService:
    def __init__(self, db_helper):
        self.db_helper = db_helper

    def create_bulk_users(self, users_data):
        with self.db_helper.get_session() as session:
            users = [User(**user_data) for user_data in users_data]
            session.bulk_save_objects(users)
            session.commit()

    def create_user(self, user_data):
        with self.db_helper.get_session() as session:
            user = User(**user_data)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                raise

    def get_user(self, user_id):
        with self.db_helper.get_session() as session:
            return session.query(User).filter_by(id=user_id).first()











# from src.models.models import User

# class UserService:
#     def __init__(self, db_helper):
#         self.db_helper = db_helper

#     def create_user(self, user_data):
#         user = User(**user_data)
#         with self.db_helper.get_session() as session:
#             session.add(user)
#             session.commit()
