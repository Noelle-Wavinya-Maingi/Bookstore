# Import necessary modules from SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base

# Define a User class that represents a table in the database
class User(Base):
    # Specify the table name in the database
    __tablename__ = "users"

    # Define the columns for the "users" table
    id = Column(Integer, primary_key=True, index=True)  
    username = Column(String, unique=True, index=True)  

    # Define relationships with other tables using the "relationship" function
    # The "borrowed_books" and "fines" relationships are defined here
    borrowed_books = relationship("BorrowedBook", back_populates="user")
    fines = relationship("Fines", back_populates="user")
