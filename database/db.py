# Import necessary modules from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the URL for the SQLite database (change this URL to your desired database)
db_url = "sqlite:///bookstore.db"

# Create a SQLAlchemy database engine using the specified URL
engine = create_engine(db_url)

# Create a session factory that will create individual database sessions
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# Create a base class for declarative SQLAlchemy models
Base = declarative_base()
