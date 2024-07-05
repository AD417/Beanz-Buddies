import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from CRUD.types import Base

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URI from environment variables
DATABASE_URI = os.getenv('DATABASE_URI')

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Create a session factory
Session = sessionmaker(bind=engine)
SESSION = Session()

Base.metadata.create_all(engine)