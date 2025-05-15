from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey,Text
from typing import List
from sqlalchemy.types import JSON
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
    pass

class title(Base):
    __tablename__='title'
    id:Mapped[int]=mapped_column(primary_key=True)
    buyer_name :Mapped[str]=mapped_column(nullable=True)
    seller_name:Mapped[str]=mapped_column(nullable=True)
    
    def __repr__(self)-> str:
        return f"<title buyer_name={self.buyer_name}>"

class poa_blueprint(Base):
    __tablename__='poa_blueprint'
    id:Mapped[int]=mapped_column(primary_key=True)
    buyer_name:Mapped[str]=mapped_column(nullable=True)
    buyer_signature:Mapped[str]=mapped_column(nullable=True)
    seller_name:Mapped[str]=mapped_column(nullable=True)
    seller_signature:Mapped[str]=mapped_column(nullable=True)
    
    def __repr__(self)-> str:
        return f"<poa_blueprint buyer_name={self.buyer_name}>"

class user_car_trade(Base):
    __tablename__="user_car_trade"
    id:Mapped[int]=mapped_column(primary_key=True)
    buyer_name:Mapped[str]=mapped_column(nullable=True)
    buyer_signature:Mapped[str]=mapped_column(nullable=True)
    seller_name:Mapped[str]=mapped_column(nullable=True)
    seller_signature:Mapped[str]=mapped_column(nullable=True)
    vnumber:Mapped[str]=mapped_column(nullable=True)
    stk:Mapped[str]=mapped_column(nullable=True)
    
    def __repr__(self)-> str:
        return f"<user_car_trade buyer_name={self.buyer_name}>"
    
# class bank_statement(Base):
#     # __tablename__="bank_details"
#     # id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
#     # ransaction_details: Mapped[dict] = mapped_column(JSON)
#     # account_summary: Mapped[dict] = mapped_column(JSON)
#     # statement_start_date:Mapped[str]=mapped_column(nullable=False)
#     # statement_end_date:Mapped[str]=mapped_column(nullable=False)
#     # branch_transit_number:Mapped[int]=mapped_column(nullable=False)
#     # bank_name:Mapped[str]=mapped_column(nullable=False)
#     # account_type:Mapped[str]=mapped_column(nullable=False)
#     # account_number:Mapped[str]=mapped_column(nullable=False)
#     # account_holder_name:Mapped[str]=mapped_column(nullable=False)
#     # account_holder_address:Mapped[str]=mapped_column(nullable=False)
    
#     __tablename__ = "bank_details"

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     transaction_details: Mapped[dict] = mapped_column(JSON)
#     account_summary: Mapped[dict] = mapped_column(JSON)
#     statement_start_date: Mapped[str] 
#     statement_end_date: Mapped[str] 
#     branch_transit_number: Mapped[int] 
#     bank_name: Mapped[str] 
#     account_type: Mapped[str] 
#     account_number: Mapped[str] 
#     account_holder_name: Mapped[str] 
#     account_holder_address: Mapped[str]
    
    
    
    
    
    