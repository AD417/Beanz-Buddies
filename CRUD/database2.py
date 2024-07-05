import os
from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URI from environment variables
DATABASE_URI = os.getenv('DATABASE_URI')

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Create a base class for declarative class definitions
Base = declarative_base()

class Pairing(Base):
    __tablename__ = "pairings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    member1 = Column(String, nullable=False)
    member2 = Column(String, nullable=False)
    last_date = Column(Date, nullable=False)

# Create the users table
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Insert sample data
now = datetime.date.today()
names = [
    "Benjamin Piro",
    "Katie Koontz",
    "Nidhi Baindur",
    "Joe Abbate",
    "Dani Saba",
    "Joe Vita",
    "Chrissy Espeleta",
    "Connor Langa",
    "Zachary Cox",
    "Ian Kopke",
    "Sam Cordry",
    "Grant Hawerlander",
    "Eva",
    "Ekam",
    "Ethan Ferguson",
    "Mary Strodl",
    "Vivian Hafener",
    "Mirai Day",
    "Asha Kadagala",
    "Emma Schmidt",
    "Gavin McConnell",
    "Jason Koser",
    "Jinna Smail",
    "Joseph Issac",
    "Matt Marafino",
    "Will Hellinger",
    "Wilson McDade",
    "Adam Newlight",
    "Darwin Tran",
    "Tyler Samay",
    "Ella Soccoli",
    "Charlotte George",
    "Randall M Guy"
]

for first in range(len(names)): 
    for second in range(first+1, len(names)):
        pair = Pairing(member1 = names[first], member2 = names[second], last_date=now)
        session.add(pair)

session.commit()
