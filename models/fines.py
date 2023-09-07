#Import necessary modules from SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from database.db import Base

#Define a Fines class that represents a table in the database
class Fines(Base):
    #Specify the table name in the database
    __tablename__ = "fines"

    #Define the colunms for the "fines" table
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount  = Column(Float)
    arrears = Column(Boolean, default=False)
    
    #Define relationship with other tables using the "relationship" function
    user = relationship("User", back_populates = "fines")
