from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class RDBMSHelper:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_all_tables(self, base):
        """
        Create all tables based on the Base metadata.
        """
        base.metadata.create_all(self.engine)

    def drop_all_tables(self, base):
        """
        Drop all tables based on the Base metadata.
        """
        base.metadata.drop_all(self.engine)

    def get_session(self):
        """
        Provide a session for database operations.
        """
        return self.Session()