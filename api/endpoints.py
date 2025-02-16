from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from elastic.elastic_search import es
from models.database import SessionLocal
from models.customer import Customer, Salesman, CustomerType, CompanyModel, PaymentTerms, CustomerGroup
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema for request & response
class CustomerBase(BaseModel):
    customer_code: str
    customer_name: str
    contact_person_name: str
    phone: str
    email: str
    credit_limit: int
    is_active: bool
    salesman_id: Optional[int]
    customer_type_id: Optional[int]
    company_name_id: Optional[int]
    payment_terms_id: Optional[int]
    customer_group_id: Optional[int]

class CustomerResponse(CustomerBase):
    id: int
    salesman_name: Optional[str]
    customer_type_name: Optional[str]
    company_name: Optional[str]
    payment_terms_name: Optional[str]
    customer_group_name: Optional[str]
    
    class Config:
        from_attributes = True  # Ensures proper ORM model serialization

# ✅ Create Customer
@router.post("/customers/", response_model=CustomerResponse)
def create_customer(customer: CustomerBase, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    # Index in Elasticsearch
    try:
        es.index(index="customers", id=db_customer.id, body=customer.dict(), refresh="wait_for")
    except Exception as e:
        print(f"⚠️ Elasticsearch Indexing Failed: {e}")

    return db_customer

# ✅ Get Customer by ID with Joins
@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = (
        db.query(Customer)
        .options(
            joinedload(Customer.salesman),
            joinedload(Customer.customer_type),
            joinedload(Customer.company_name),
            joinedload(Customer.payment_terms),
            joinedload(Customer.customer_group),
        )
        .filter(Customer.id == customer_id)
        .first()
    )
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return CustomerResponse(
        id=customer.id,
        customer_code=customer.customer_code,
        customer_name=customer.customer_name,
        contact_person_name=customer.contact_person_name,
        phone=customer.phone,
        email=customer.email,
        credit_limit=customer.credit_limit,
        is_active=customer.is_active,
        salesman_id=customer.salesman_id,
        salesman_name=customer.salesman.name if customer.salesman else None,
        customer_type_name=customer.customer_type.customer_type if customer.customer_type else None,
        company_name=customer.company_name.name if customer.company_name else None,
        payment_terms_name=customer.payment_terms.term_name if customer.payment_terms else None,
        customer_group_name=customer.customer_group.customer_group_name if customer.customer_group else None,
    )

# ✅ Search Customers in Elasticsearch
@router.get("/customers/search/")
def search_customers(query: str):
    try:
        response = es.search(index="customers", body={"query": {"match": {"customer_name": query}}})
        return [hit["_source"] for hit in response.get("hits", {}).get("hits", [])]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Elasticsearch search failed: {e}")

# ✅ Get All Customers with Filtering
@router.get("/customers/", response_model=List[CustomerResponse])
def get_all_customers(
    is_active: Optional[bool] = None,
    min_credit_limit: Optional[int] = None,
    max_credit_limit: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Customer)
    
    if is_active is not None:
        query = query.filter(Customer.is_active == is_active)
    if min_credit_limit is not None:
        query = query.filter(Customer.credit_limit >= min_credit_limit)
    if max_credit_limit is not None:
        query = query.filter(Customer.credit_limit <= max_credit_limit)
    
    return query.all()

# ✅ Update Customer
@router.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: CustomerBase, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in customer.dict().items():
        setattr(db_customer, key, value)
    
    db.commit()
    db.refresh(db_customer)

    # Update Elasticsearch
    try:
        es.index(index="customers", id=customer_id, body=customer.dict(), refresh="wait_for")
    except Exception as e:
        print(f"⚠️ Elasticsearch Update Failed: {e}")

    return db_customer

# ✅ Delete Customer
@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(db_customer)
    db.commit()

    # Remove from Elasticsearch
    try:
        es.delete(index="customers", id=customer_id, ignore=[404])
    except Exception as e:
        print(f"⚠️ Elasticsearch Delete Failed: {e}")

    return {"message": "Customer deleted successfully"}















# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from elastic.elastic_search import es
# from models.database import SessionLocal
# from models.customer import Customer
# from pydantic import BaseModel
# from typing import List, Optional

# router = APIRouter()

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Pydantic schema for request & response
# class CustomerBase(BaseModel):
#     customer_code: str
#     customer_name: str
#     contact_person_name: str
#     phone: str
#     email: str
#     credit_limit: int
#     is_active: bool

# class CustomerResponse(CustomerBase):
#     id: int

#     class Config:
#         from_attributes = True  # Ensures proper ORM model serialization

# # ✅ Create Customer
# @router.post("/customers/", response_model=CustomerResponse)
# def create_customer(customer: CustomerBase, db: Session = Depends(get_db)):
#     db_customer = Customer(**customer.dict())
#     db.add(db_customer)
#     db.commit()
#     db.refresh(db_customer)

#     # Index in Elasticsearch
#     try:
#         es.index(index="customers", id=db_customer.id, body=customer.dict(), refresh="wait_for")
#     except Exception as e:
#         print(f"⚠️ Elasticsearch Indexing Failed: {e}")

#     return db_customer

# # ✅ Get Customer by ID
# @router.get("/customers/{customer_id}", response_model=CustomerResponse)
# def get_customer(customer_id: int, db: Session = Depends(get_db)):
#     customer = db.query(Customer).filter(Customer.id == customer_id).first()
#     if not customer:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     return customer

# # ✅ Search Customers in Elasticsearch
# @router.get("/customers/search/")
# def search_customers(query: str):
#     try:
#         response = es.search(index="customers", body={"query": {"match": {"customer_name": query}}})
#         return [hit["_source"] for hit in response.get("hits", {}).get("hits", [])]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Elasticsearch search failed: {e}")

# # ✅ Get All Customers
# @router.get("/customers/", response_model=List[CustomerResponse])
# def get_all_customers(db: Session = Depends(get_db)):
#     customers = db.query(Customer).all()
#     return customers  # No need for explicit 404; empty list is fine

# # ✅ Update Customer
# @router.put("/customers/{customer_id}", response_model=CustomerResponse)
# def update_customer(customer_id: int, customer: CustomerBase, db: Session = Depends(get_db)):
#     db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
#     if not db_customer:
#         raise HTTPException(status_code=404, detail="Customer not found")

#     for key, value in customer.dict().items():
#         setattr(db_customer, key, value)

#     db.commit()
#     db.refresh(db_customer)

#     # Update Elasticsearch
#     try:
#         es.index(index="customers", id=customer_id, body=customer.dict(), refresh="wait_for")
#     except Exception as e:
#         print(f"⚠️ Elasticsearch Update Failed: {e}")

#     return db_customer

# # ✅ Delete Customer
# @router.delete("/customers/{customer_id}")
# def delete_customer(customer_id: int, db: Session = Depends(get_db)):
#     db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
#     if not db_customer:
#         raise HTTPException(status_code=404, detail="Customer not found")

#     db.delete(db_customer)
#     db.commit()

#     # Remove from Elasticsearch
#     try:
#         es.delete(index="customers", id=customer_id, ignore=[404])
#     except Exception as e:
#         print(f"⚠️ Elasticsearch Delete Failed: {e}")

#     return {"message": "Customer deleted successfully"}
