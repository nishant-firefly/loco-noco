from elasticsearch import Elasticsearch
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.customer import Customer
import os

# Load Elasticsearch URL from environment variables
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
es = Elasticsearch(ELASTICSEARCH_URL)

def create_index():
    """Create 'customers' index in Elasticsearch if it doesn't exist"""
    index_body = {
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "customer_code": {"type": "keyword"},
                "customer_name": {"type": "text"},
                "contact_person_name": {"type": "text"},
                "salesman_id": {"type": "integer"},
                "customer_type_id": {"type": "integer"},
                "company_name_id": {"type": "integer"},
                "phone": {"type": "keyword"},
                "email": {"type": "text"},
                "fax": {"type": "keyword"},
                "payment_terms_id": {"type": "integer"},
                "customer_group_id": {"type": "integer"},
                "credit_limit": {"type": "integer"},
                "product_promotion_id": {"type": "integer"},
                "customer_note": {"type": "text"},
                "is_active": {"type": "boolean"},
                "is_msa_include": {"type": "boolean"},
                "is_sales_tax_applicable": {"type": "boolean"},
                "send_email_on_invoice_creation": {"type": "boolean"},
            }
        }
    }

    if not es.indices.exists(index="customers"):
        es.indices.create(index="customers", body=index_body)
        print("✅ Created 'customers' index")
    else:
        print("ℹ️ 'customers' index already exists")

def index_customers():
    """Fetch customers from PostgreSQL and index them in Elasticsearch"""
    db: Session = SessionLocal()
    customers = db.query(Customer).all()

    for customer in customers:
        doc = {
            "id": customer.id,
            "customer_code": customer.customer_code,
            "customer_name": customer.customer_name,
            "contact_person_name": customer.contact_person_name,
            "salesman_id": customer.salesman_id,
            "customer_type_id": customer.customer_type_id,
            "company_name_id": customer.company_name_id,
            "phone": customer.phone,
            "email": customer.email,
            "fax": customer.fax,
            "payment_terms_id": customer.payment_terms_id,
            "customer_group_id": customer.customer_group_id,
            "credit_limit": customer.credit_limit,
            "product_promotion_id": customer.product_promotion_id,
            "customer_note": customer.customer_note,
            "is_active": customer.is_active,
            "is_msa_include": customer.is_msa_include,
            "is_sales_tax_applicable": customer.is_sales_tax_applicable,
            "send_email_on_invoice_creation": customer.send_email_on_invoice_creation,
        }
        es.index(index="customers", id=customer.id, body=doc)

    print(f"✅ Indexed {len(customers)} customers in Elasticsearch")
    db.close()

if __name__ == "__main__":
    create_index()
    index_customers()





# from elasticsearch import Elasticsearch
# import os
# import time

# ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
# es = Elasticsearch(ELASTICSEARCH_URL)

# # Wait for Elasticsearch to be ready
# for _ in range(5):
#     if es.ping():
#         print("✅ Connected to Elasticsearch")
#         break
#     print("⏳ Waiting for Elasticsearch to be ready...")
#     time.sleep(5)
# else:
#     raise ConnectionError("❌ Could not connect to Elasticsearch")

# def create_index():
#     index_body = {
#         "mappings": {
#             "properties": {
#                 "id": {"type": "integer"},
#                 "customer_code": {"type": "keyword"},
#                 "customer_name": {"type": "text"},
#                 "contact_person_name": {"type": "text"},
#                 "phone": {"type": "keyword"},
#                 "email": {"type": "text"},
#                 "credit_limit": {"type": "integer"},
#                 "is_active": {"type": "boolean"}
#             }
#         }
#     }
#     if not es.indices.exists(index="customers"):
#         es.indices.create(index="customers", body=index_body)
#         print("✅ Created 'customers' index")
#     else:
#         print("ℹ️ 'customers' index already exists")
