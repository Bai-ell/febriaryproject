from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float)
    brand = Column(String)
    discount = Column(Float)
    rating = Column(Float)
    volume = Column(String)
    supplier_id = Column(Integer)
    feedback_count = Column(Integer)
    valuation = Column(String)

    __table_args__ = (
        UniqueConstraint('name', 'price', name='_name_price_uc'),
    )