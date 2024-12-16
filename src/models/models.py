# SQLAlchemy models based on the Excel schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, CheckConstraint('age >= 0'), nullable=False)

    # Relationships
    orders = relationship('Order', back_populates='user')

# Product model
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, CheckConstraint('price >= 0'), nullable=False)

    # Relationships
    orders = relationship('Order', back_populates='product')

# Order model
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, CheckConstraint('quantity > 0'), nullable=False)

    # Relationships
    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')




