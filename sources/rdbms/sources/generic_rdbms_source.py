from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

class GenericRDBMSSource:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create(self, model, data):
        session = self.Session()
        try:
            record = model(**data)
            session.add(record)
            session.commit()
            session.refresh(record)
            return record
        except SQLAlchemyError as e:
            print(f"Database error during create: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def read(self, model, record_id):
        session = self.Session()
        try:
            return session.get(model, record_id)
        except SQLAlchemyError as e:
            print(f"Database error during read: {e}")
            raise
        finally:
            session.close()

    def filter(self, model, filters):
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
        session = self.Session()
        try:
            record = session.get(model, record_id)
            if not record:
                raise ValueError(f"Record with id {record_id} not found")
            for field, value in update_fields.items():
                setattr(record, field, value)
            session.commit()
        except SQLAlchemyError as e:
            print(f"Database error during update: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def delete(self, model, record_id):
        session = self.Session()
        try:
            record = session.get(model, record_id)
            if not record:
                raise ValueError(f"Record with id {record_id} not found")
            session.delete(record)
            session.commit()
        except SQLAlchemyError as e:
            print(f"Database error during delete: {e}")
            session.rollback()
            raise
        finally:
            session.close()








# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import SQLAlchemyError

# class GenericRDBMSSource:
#     def __init__(self, db_url):
#         """
#         Initialize the database connection and sessionmaker.

#         Args:
#             db_url: Database connection string.
#         """
#         self.engine = create_engine(db_url)
#         self.Session = sessionmaker(bind=self.engine)

#     def create(self, model, data):
#         """
#         Create a new record in the database.

#         Args:
#             model: SQLAlchemy model to insert into.
#             data: Dictionary of field-value pairs for the new record.

#         Returns:
#             The newly created record.
#         """
#         session = self.Session()
#         try:
#             record = model(**data)
#             session.add(record)
#             session.commit()
#             session.refresh(record)
#             return record
#         except SQLAlchemyError as e:
#             print(f"Database error during create: {e}")
#             session.rollback()
#             raise
#         finally:
#             session.close()

#     def read(self, model, record_id):
#         """
#         Read a record by its primary key.

#         Args:
#             model: SQLAlchemy model to query.
#             record_id: ID of the record to retrieve.

#         Returns:
#             The record if found, or None.
#         """
#         session = self.Session()
#         try:
#             return session.get(model, record_id)
#         except SQLAlchemyError as e:
#             print(f"Database error during read: {e}")
#             raise
#         finally:
#             session.close()

#     def filter(self, model, filters):
#         """
#         Fetch records based on the given filters.

#         Args:
#             model: SQLAlchemy model to query.
#             filters: Dictionary of field-value pairs for filtering.

#         Returns:
#             List of records matching the filters.
#         """
#         session = self.Session()
#         try:
#             query = session.query(model)
#             for field, value in filters.items():
#                 query = query.filter(getattr(model, field) == value)
#             return query.all()
#         except SQLAlchemyError as e:
#             print(f"Database error during filter: {e}")
#             raise
#         finally:
#             session.close()

#     def update(self, model, record_id, update_fields):
#         """
#         Update a record with the specified fields.

#         Args:
#             model: SQLAlchemy model to query.
#             record_id: ID of the record to update.
#             update_fields: Dictionary of field-value pairs to update.

#         Raises:
#             ValueError: If the record is not found.
#         """
#         session = self.Session()
#         try:
#             record = session.get(model, record_id)
#             if not record:
#                 raise ValueError(f"Record with id {record_id} not found")
#             for field, value in update_fields.items():
#                 setattr(record, field, value)
#             session.commit()
#         except SQLAlchemyError as e:
#             print(f"Database error during update: {e}")
#             session.rollback()
#             raise
#         finally:
#             session.close()

#     def delete(self, model, record_id):
#         """
#         Delete a record by its primary key.

#         Args:
#             model: SQLAlchemy model to query.
#             record_id: ID of the record to delete.

#         Raises:
#             ValueError: If the record is not found.
#         """
#         session = self.Session()
#         try:
#             record = session.get(model, record_id)
#             if not record:
#                 raise ValueError(f"Record with id {record_id} not found")
#             session.delete(record)
#             session.commit()
#         except SQLAlchemyError as e:
#             print(f"Database error during delete: {e}")
#             session.rollback()
#             raise
#         finally:
#             session.close()
