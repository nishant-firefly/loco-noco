from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from models.database import Base

US_STATES = [
        ('Alabama', 'Alabama'),
        ('Alaska', 'Alaska'),
        ('Arizona', 'Arizona'),
        ('Arkansas', 'Arkansas'),
        ('California', 'California'),
        ('Colorado', 'Colorado'),
        ('Connecticut', 'Connecticut'),
        ('Delaware', 'Delaware'),
        ('Florida', 'Florida'),
        ('Georgia', 'Georgia'),
        ('Hawaii', 'Hawaii'),
        ('Idaho', 'Idaho'),
        ('Illinois', 'Illinois'),
        ('Indiana', 'Indiana'),
        ('Iowa', 'Iowa'),
        ('Kansas', 'Kansas'),
        ('Kentucky', 'Kentucky'),
        ('Louisiana', 'Louisiana'),
        ('Maine', 'Maine'),
        ('Maryland', 'Maryland'),
        ('Massachusetts', 'Massachusetts'),
        ('Michigan', 'Michigan'),
        ('Minnesota', 'Minnesota'),
        ('Mississippi', 'Mississippi'),
        ('Missouri', 'Missouri'),
        ('Montana', 'Montana'),
        ('Nebraska', 'Nebraska'),
        ('Nevada', 'Nevada'),
        ('New Hampshire', 'New Hampshire'),
        ('New Jersey', 'New Jersey'),
        ('New Mexico', 'New Mexico'),
        ('New York', 'New York'),
        ('North Carolina', 'North Carolina'),
        ('North Dakota', 'North Dakota'),
        ('Ohio', 'Ohio'),
        ('Oklahoma', 'Oklahoma'),
        ('Oregon', 'Oregon'),
        ('Pennsylvania', 'Pennsylvania'),
        ('Rhode Island', 'Rhode Island'),
        ('South Carolina', 'South Carolina'),
        ('South Dakota', 'South Dakota'),
        ('Tennessee', 'Tennessee'),
        ('Texas', 'Texas'),
        ('Utah', 'Utah'),
        ('Vermont', 'Vermont'),
        ('Virginia', 'Virginia'),
        ('Washington', 'Washington'),
        ('West Virginia', 'West Virginia'),
        ('Wisconsin', 'Wisconsin'),
        ('Wyoming', 'Wyoming'),
    ]




class Salesman(Base):
    __tablename__ = "salesman"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class CompanyModel(Base):
    __tablename__ = "customer_company_name"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class CustomerType(Base):
    __tablename__ = "customer_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_type = Column(String(255), nullable=False)
    cash_and_carry_percentage = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)


class PaymentTerms(Base):
    __tablename__ = "payment_terms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    term_name = Column(String(255), nullable=False)


class CustomerGroup(Base):
    __tablename__ = "customer_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_group_code = Column(String(255), unique=True, nullable=False)
    customer_group_name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    zipcode = Column(String(255), nullable=False)


class ProductPromotion(Base):
    __tablename__ = "product_promotion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(255), nullable=False)


class PricingModel(Base):
    __tablename__ = "pricing_model"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_code = Column(String(255), unique=True, index=True, nullable=False)
    customer_name = Column(String(255), nullable=False)
    contact_person_name = Column(String(255), nullable=False)
    salesman_id = Column(Integer, ForeignKey("salesman.id"), nullable=True)
    customer_type_id = Column(Integer, ForeignKey("customer_type.id"), nullable=True)
    company_name_id = Column(Integer, ForeignKey("customer_company_name.id"), nullable=True)
    phone = Column(String(15), nullable=False)
    email = Column(String(255), nullable=False)
    fax = Column(String(20), nullable=True)
    payment_terms_id = Column(Integer, ForeignKey("payment_terms.id"), nullable=True)
    customer_group_id = Column(Integer, ForeignKey("customer_group.id"), nullable=True)
    credit_limit = Column(Integer, default=0)
    product_promotion_id = Column(Integer, ForeignKey("product_promotion.id"), nullable=True)

    customer_note = Column(Text, nullable=True)
    is_active = Column(Boolean, default=False)
    is_msa_include = Column(Boolean, default=False)
    is_sales_tax_applicable = Column(Boolean, default=False)
    send_email_on_invoice_creation = Column(Boolean, default=False)

    # Relationships
    salesman = relationship("Salesman")
    customer_type = relationship("CustomerType")
    company_name = relationship("CompanyModel")
    payment_terms = relationship("PaymentTerms")
    customer_group = relationship("CustomerGroup")
    product_promotion = relationship("ProductPromotion")






# from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
# from sqlalchemy.orm import relationship
# from models.database import Base

# class Customer(Base):
#     __tablename__ = "customer"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     customer_code = Column(String(255), unique=True, index=True, nullable=False)
#     customer_name = Column(String(255), nullable=False)
#     contact_person_name = Column(String(255), nullable=False)
#     salesman_id = Column(Integer, ForeignKey("salesman.id"), nullable=True)
#     customer_type_id = Column(Integer, ForeignKey("customer_type.id"), nullable=True)
#     company_name_id = Column(Integer, ForeignKey("company.id"), nullable=True)
#     phone = Column(String(15), nullable=False)
#     email = Column(String(255), nullable=False)
#     fax = Column(String(20), nullable=True)
#     payment_terms_id = Column(Integer, ForeignKey("payment_terms.id"), nullable=True)
#     customer_group_id = Column(Integer, ForeignKey("customer_group.id"), nullable=True)
#     credit_limit = Column(Integer, default=0)
#     product_promotion_id = Column(Integer, ForeignKey("product_promotion.id"), nullable=True)

#     customer_note = Column(Text, nullable=True)
#     is_active = Column(Boolean, default=False)
#     is_msa_include = Column(Boolean, default=False)
#     is_sales_tax_applicable = Column(Boolean, default=False)
#     send_email_on_invoice_creation = Column(Boolean, default=False)
