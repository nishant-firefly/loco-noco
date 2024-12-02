from ..helpers.rdbms_helper import RDBMSHelper
from .base_rdbms_source import BaseRDBMSSource

class GenericRDBMSSource(BaseRDBMSSource):
    def __init__(self, db_url):
        self.helper = RDBMSHelper(db_url)

    def auth(self, credentials=None):
        self.db_url = credentials.get("db_url")
        print(f"Authenticated with DB URL: {self.db_url}")

    def connect(self):
        print(f"Connected to database at {self.db_url}.")

    def filter(self, model, criteria):
        with self.helper.get_session() as session:
            return session.query(model).filter_by(**criteria).all()

    def update(self, model, obj_id, updates):
        with self.helper.get_session() as session:
            obj = session.query(model).get(obj_id)
            if obj:
                for key, value in updates.items():
                    setattr(obj, key, value)

    def delete(self, model, obj_id):
        with self.helper.get_session() as session:
            obj = session.query(model).get(obj_id)
            if obj:
                session.delete(obj)
