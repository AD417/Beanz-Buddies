from __future__ import annotations
from datetime import date

from sqlalchemy import and_, func

from CRUD.types import Pairing, User
from CRUD.saving import SESSION


class Database:
    """A basic CRUD system to store all pairing entries."""

    # CREATE

    def add_pair(self: Database, first: str, second: str, time: date = date.today) -> Pairing:
        """Add a match pair to the database."""
        if first == second: raise ValueError(f"Cannot pair a person '{first}' with themself!")

        pair = Pairing(member1=first, member2=second, date=date.min)
        SESSION.add(pair)
        return pair

    def force_save(self: Database):
        SESSION.commit()

    # READ

    def get_recent_pair(self: Database, first: str, second: str) -> Pairing | None:
        """
        Get the data regarding the most recent pairing of two members in 
        the database.
        If no such pairing exists, returns "None".
        """
        if first == second: return None

        most_recent = SESSION.query(Pairing) \
                .filter(Pairing.member1 in (first, second)) \
                .filter(Pairing.member2 in (first, second)) \
                .order_by(Pairing.date.desc()) \
                .first()

        return most_recent
    
    def get_all_pairs(self: Database, first: str, second: str) -> list[Pairing]:
        """Get all data involving this pair. This list is NOT sorted."""
        if first == second: return []
        return SESSION.query(Pairing) \
                .filter(Pairing.member1 in (first, second)) \
                .filter(Pairing.member2 in (first, second)) \
                .all()

    def get_pairs_with(self: Database, name: str) -> list[Pairing]:
        """Get all pairings involving """
        return SESSION.query(Pairing) \
                .filter(Pairing.member1 == name or Pairing.member2 == name) \
                .all()
    
    def get_all_pairs_involving(self: Database, names: list[str]) -> list[Pairing]:
        """Get all pairs that only involve the names listed."""
        # I blame chatgpt when this breaks.
        subquery = (
            SESSION.query(
                Pairing.member1,
                Pairing.member2,
                func.max(Pairing.last_date).label('max_last_date')
            )
            .group_by(Pairing.member1, Pairing.member2)
            .subquery()
        )

        query = (
            SESSION.query(Pairing)
            .join(
                subquery,
                and_(
                    Pairing.member1 == subquery.c.member1,
                    Pairing.member2 == subquery.c.member2,
                    Pairing.last_date == subquery.c.max_last_date
                )
            )
            .filter(
                Pairing.member1.in_(names),
                Pairing.member2.in_(names)
            )
        )

        return query.all()

    def close(save: bool = True):
        if save: SESSION.commit()
        SESSION.close()

    # Other stuff

    def pair_weight(self: Database, first: str, second: str, now: date) -> float:
        """Determine the weight given to a pair of people."""
        
        pair = self.get_recent_pair(first, second)
        if pair is None:
            return 1.0
        
        return pair.weight(now)
    '''

    # UPDATING

    def set_pair(self: Database, first: str, second: str, entry: Entry):
        if first < second: 
            first, second = second, first
        
        self._data[(first, second)] = entry

    def set_pair_date(self: Database, first: str, second: str, day: date):
        entry = self.get_recent_pair(first, second)
        entry = entry.update_last_meeting(day, True) # TODO
        self.set_pair(first, second, entry)

    # Other stuff

    def pair_weight(self: Database, first: str, second: str, now: date) -> float:
        """Determine the weight given to a pair of people."""
        
        entry = self.get_recent_pair(first, second)
        return entry.pair_weight(now)
'''
