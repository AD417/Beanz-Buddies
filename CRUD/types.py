from __future__ import annotations
from datetime import date, timedelta
from sqlalchemy import Column, Date, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import enum

# Create a base class for declarative class definitions
Base = declarative_base()

class PairData(Base):
    __tablename__ = "pairings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    member1 = Column(String, nullable=False)
    member2 = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    def weight(self: PairData, now: date) -> float:
        elapsed_time = now - self.last_meeting

        # If the last meeting was more recent, don't bother.
        EARLY = timedelta(days=14)
        # If the last meeting was less recent, then time decay is irrelevant.
        LATE = timedelta(days=90)

        if elapsed_time <= EARLY:
            return 0
        if elapsed_time >= LATE:
            return 1
        
        recency_factor = (elapsed_time - EARLY) / (LATE - EARLY)
        return recency_factor * recency_factor
        

class Role(enum.Enum):
    freshman = 1
    upperclassman = 2
    alumni = 3
    other = 4

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)