# Multi DB Query Builder API

A powerful, unified query builder for multiple databases, including PostgreSQL, MySQL, MSSQL, Oracle, and Elasticsearch. Built with FastAPI and SQLAlchemy.

## Features
Unified query builder for multiple databases  
FastAPI-based RESTful API  
Role-based user management  
Elasticsearch indexing and search  
Database-agnostic CRUD operations  
Microservices-friendly architecture  

## Installation

Clone the repository:

git clone https://github.com/nishant-firefly/loco-noco.git
Branch Name: multi_DB_QueryBuilder
cd multi-db-query-builder




## requirements
pip install -r requirements.txt


## docker
docker-compose start

## using Alembic for migrations, apply them:
alembic revision --autogenerate -m "Create users table"
alembic upgrade head






## Run API and Test with Different Databases

uvicorn api:app --reload


## Change this to "postgres", "mysql", "mssql", "oracle" as needed,now postgres is selected.