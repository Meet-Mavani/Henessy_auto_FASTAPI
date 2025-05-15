from sqlalchemy.orm import Session
from Database.schema.connect import engine

# Create a session factory instead of a global session
session = Session(bind=engine)