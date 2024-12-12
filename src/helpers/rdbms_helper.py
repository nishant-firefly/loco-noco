# General RDBMS helper (SQLAlchemy-based)
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class RDBMSHelper:
    def __init__(self, db_url):
        """
        Initialize the RDBMS helper with a database URL.
        :param db_url: Database connection string
        """
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self):
        """
        Provide a database session for operations.
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def create_all_tables(self, base):
        """
        Create all tables defined in the SQLAlchemy Base.
        :param base: SQLAlchemy declarative Base object
        """
        base.metadata.create_all(self.engine)

    def drop_all_tables(self, base):
        """
        Drop all tables defined in the SQLAlchemy Base.
        :param base: SQLAlchemy declarative Base object
        """
        base.metadata.drop_all(self.engine)
