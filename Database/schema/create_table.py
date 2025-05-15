# from starting_schema import Base,title,poa_blueprint,user_car_trade

from Database.schema.starting_schema import Base,title,poa_blueprint,user_car_trade
from Database.schema.connect import engine

print("Creating the table")
Base.metadata.create_all(bind=engine)
# Base.metadata.create_all(bind=engine)

# from sqlalchemy import create_engine
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from sqlalchemy import String, Integer

# # Define the database engine (use your actual DB URI here)
# engine = create_engine("sqlite:///example.db", echo=True)  # Update DB URI as needed

# # Base class
# class Base(DeclarativeBase):
#     pass

# # Model definition
# class user_car_trade(Base):
#     __tablename__ = "user_car_trade"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     buyer_name: Mapped[str] = mapped_column(nullable=True)
#     buyer_signature: Mapped[str] = mapped_column(nullable=True)
#     seller_name: Mapped[str] = mapped_column(nullable=True)
#     seller_signature: Mapped[str] = mapped_column(nullable=True)
#     vin: Mapped[str] = mapped_column(nullable=True)
#     stk: Mapped[str] = mapped_column(nullable=True)

# # Create the table
# Base.metadata.create_all(bind=engine)
