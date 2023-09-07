#Import necessary modules from SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from database.db import Base

#Define a Book class that represents a table in the database
class Book(Base):
    #Specify the table name in the database
    __tablename__ = "books"

    #Define the columns for the "books" table
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    status = Column(Boolean, default=True)
    inventory = Column(Integer, default = 0)
    price = Column(Float, default = 0.0)
    total_sales = Column(Integer, default=0)

    #Define relationships with other tables using the "relationship" function
    borrowed_books = relationship("BorrowedBook", back_populates="book")
    sales = relationship("Sales", back_populates = "book")