#Import necessary modules from SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from database.db import Base

#Define a Sales class that represents a table in the database
class Sales(Base):
    #Specify the table name in the database
    __tablename__ = "sales"

    #Define the columns for the "sales" table
    id = Column(Integer, primary_key = True, index= True)
    book_id = Column(Integer, ForeignKey("books.id"))
    quantity = Column(Integer, default = 0)
    total_amount = Column(Float, default = 0.0)

    #Define the relationship with other tables using the "relationship" function
    book = relationship("Book", back_populates = "sales")
