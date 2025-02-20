## Clone the Repository **
git clone https://github.com/nishant-firefly/loco-noco.git

## Branch Name **
elastic-search 


## Install Dependencies
pip install -r requirements.txt

## Migrations **

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

## start docker
docker-compose up --build -d


 ## Run FastAPI Server **
uvicorn main:app --reload

## Start Elasticsearch
http://localhost:9200/customer/

## Check in Command Prompt **

curl -X GET "http://localhost:9200/customer/_search?pretty"

