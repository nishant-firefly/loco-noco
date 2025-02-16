

from fastapi import FastAPI
from api.endpoints import router
from elastic.elastic_search import create_index

app = FastAPI()

app.include_router(router)

# Create Elasticsearch index on startup
@app.on_event("startup")
def startup():
    create_index()

@app.get("/")
def home():
    return {"message": "Customer API is running"}
