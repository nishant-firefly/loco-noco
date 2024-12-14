# CRUD operations abstraction

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class GenericRDBMSSource:
    def __init__(self, db_url):
        """
        Initialize the RDBMS source with a database URL.
        :param db_url: Database connection string
        """
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create(self, model, data):
        """
        Create a new record in the database.
        :param model: SQLAlchemy model class
        :param data: Dictionary of data to insert
        :return: Created record
        """
        session = self.Session()
        try:
            record = model(**data)
            session.add(record)
            session.commit()
            session.refresh(record)
            return record
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error during create: {e}")
            raise
        finally:
            session.close()

    def read(self, model, record_id):
        """
        Read a record from the database by ID.
        :param model: SQLAlchemy model class
        :param record_id: ID of the record to read
        :return: Record object or None
        """
        session = self.Session()
        try:
            return session.get(model, record_id)
        except SQLAlchemyError as e:
            print(f"Database error during read: {e}")
            raise
        finally:
            session.close()

    def filter(self, model, filters):
        """
        Filter records in the database by given criteria.
        :param model: SQLAlchemy model class
        :param filters: Dictionary of field-value pairs for filtering
        :return: List of filtered records
        """
        session = self.Session()
        try:
            query = session.query(model)
            for field, value in filters.items():
                query = query.filter(getattr(model, field) == value)
            return query.all()
        except SQLAlchemyError as e:
            print(f"Database error during filter: {e}")
            raise
        finally:
            session.close()

    def update(self, model, record_id, update_fields):
        """
        Update a record in the database.
        :param model: SQLAlchemy model class
        :param record_id: ID of the record to update
        :param update_fields: Dictionary of fields to update
        :return: Updated record
        """
        session = self.Session()
        try:
            record = session.get(model, record_id)
            if not record:
                raise ValueError(f"Record with id {record_id} not found")
            for field, value in update_fields.items():
                setattr(record, field, value)
            session.commit()
            session.refresh(record)
            return record
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error during update: {e}")
            raise
        finally:
            session.close()

    def delete(self, model, record_id):
        """
        Delete a record from the database by ID.
        :param model: SQLAlchemy model class
        :param record_id: ID of the record to delete
        """
        session = self.Session()
        try:
            record = session.get(model, record_id)
            if not record:
                raise ValueError(f"Record with id {record_id} not found")
            session.delete(record)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error during delete: {e}")
            raise
        finally:
            session.close()




