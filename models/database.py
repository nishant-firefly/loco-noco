from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin@localhost:5432/mydatabase")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base:
    __abstract__ = True  # Ensures SQLAlchemy does not create a table for this class

    @classmethod
    def create(cls, **kwargs):
        """Implicitly create and commit an object."""
        db = SessionLocal()
        try:
            obj = cls(**kwargs)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @classmethod
    def get(cls, obj_id):
        """Fetch an object by ID."""
        db = SessionLocal()
        try:
            return db.query(cls).filter_by(id=obj_id).first()
        finally:
            db.close()

    @classmethod
    def get_all(cls, limit=10, offset=0):
        """Fetch all objects with pagination."""
        db = SessionLocal()
        try:
            return db.query(cls).limit(limit).offset(offset).all()
        finally:
            db.close()

    @classmethod
    def update(cls, obj_id, **kwargs):
        """Update an object by ID."""
        db = SessionLocal()
        try:
            obj = db.query(cls).filter_by(id=obj_id).first()
            if obj:
                for key, value in kwargs.items():
                    setattr(obj, key, value)
                db.commit()
                db.refresh(obj)
            return obj
        finally:
            db.close()

    @classmethod
    def delete(cls, obj_id):
        """Delete an object by ID."""
        db = SessionLocal()
        try:
            obj = db.query(cls).filter_by(id=obj_id).first()
            if obj:
                db.delete(obj)
                db.commit()
            return obj
        finally:
            db.close()

Base = declarative_base(cls=Base)