from datetime import date
from CRUD import *
"""
db = load("beanz_buddies.json")

names = get_slack_channel_members()
'''[
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
    "Bonus guy"
]'''

now = date.today()

pairs = generate_pairs(db, names, now)

for first, second in pairs:
    setup_dm(first, second)
    # ...

    db.set_pair_date(first, second, now)

save(db, "beanz_buddies.json")"""


import os
from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import uuid

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URI from environment variables
DATABASE_URI = os.getenv('DATABASE_URI')

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Create a base class for declarative class definitions
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String, nullable=False)
    opt_out = Column(Boolean, default=False)

# Create the users table
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Insert sample data
user1 = User(uuid=uuid.uuid4(), role='freshman', opt_out=False)
user2 = User(uuid=uuid.uuid4(), role='upperclassman', opt_out=True)
user3 = User(uuid=uuid.uuid4(), role='alumni', opt_out=False)

session.add_all([user1, user2, user3])
session.commit()

# Query the data
users = session.query(User).all()
for user in users:
    print(f'UUID: {user.uuid}, Role: {user.role}, Opt-Out: {user.opt_out}')

# Close the session
session.close()