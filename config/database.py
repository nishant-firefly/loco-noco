from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from elasticsearch import Elasticsearch

DATABASES = {
    "postgres": "postgresql://test_user:test_password@localhost:5432/test_db",
    "mysql": "mysql+pymysql://test_user:test_password@localhost:3306/test_db",
    "mssql": "mssql+pyodbc://SA:Test@1234@localhost:1433/test_db?driver=ODBC+Driver+17+for+SQL+Server",
    "oracle": "oracle+cx_oracle://test_user:test_password@localhost:1521/XEPDB1",
}

def get_engine(db_type):
    return create_engine(DATABASES[db_type])

def get_session(db_type):
    engine = get_engine(db_type)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

# Elasticsearch connection
es = Elasticsearch(["http://localhost:9200"])







