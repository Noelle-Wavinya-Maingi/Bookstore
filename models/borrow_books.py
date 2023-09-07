#Import necessary modules from SQLAlchemy
from sqlalchemy import Column, Integer,ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.db import Base

#Deine a BorrowedBook class that represents a table in the database
class BorrowedBook(Base):
    #Specify the table name in the database
    __tablename__ = "borrowed_books"

    #Define the columns for the "borrowed_books" table
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    return_date = Column(DateTime)

    #Define relationships with other tables using the "relationship" function
    user = relationship("User", back_populates="borrowed_books")
    book = relationship("Book", back_populates="borrowed_books")