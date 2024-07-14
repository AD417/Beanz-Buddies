from __future__ import annotations
from datetime import date
import functools

from sqlalchemy import and_, func

from CRUD.types import PairData, User
from CRUD.saving import SESSION


class Database:
    """A basic CRUD system to store all pairing entries."""

    def __init__(self: Database):
        self.__cache = {}

    def cache_result(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Create a cache key based on function arguments
            cache_key = (func.__name__, args, frozenset(kwargs.items()))
            
            # Check if the result is already in the cache
            if cache_key in self.__cache:
                return self.__cache[cache_key]
            
            # Call the actual function and store the result in the cache
            result = func(self, *args, **kwargs)
            self.__cache[cache_key] = result
            return result
        return wrapper

    def invalidate_cache(self: Database):
        """Invalidates the cache, requiring future calls to actually be sent."""
        self.__cache = {}

    # CREATE

    def add_pair(self: Database, first: str, second: str, time: date = date.today) -> PairData:
        """Add a match pair to the database."""
        if first == second: raise ValueError(f"Cannot pair a person '{first}' with themself!")

        pair = PairData(member1=first, member2=second, date=date.min)
        SESSION.add(pair)
        return pair

    def force_save(self: Database):
        SESSION.commit()
        self.invalidate_cache()

    # READ

    @cache_result
    def get_recent_pair(self: Database, first: str, second: str) -> PairData | None:
        """
        Get the data regarding the most recent pairing of two members in 
        the database.
        If no such pairing exists, returns "None".
        """
        if first == second: return None

        most_recent = SESSION.query(PairData) \
                .filter(PairData.member1 in (first, second)) \
                .filter(PairData.member2 in (first, second)) \
                .order_by(PairData.date.desc()) \
                .first()

        return most_recent
    
    @cache_result
    def get_all_pairs(self: Database, first: str, second: str) -> list[PairData]:
        """Get all data involving this pair. This list is NOT sorted."""
        if first == second: return []
        return SESSION.query(PairData) \
                .filter(PairData.member1 in (first, second)) \
                .filter(PairData.member2 in (first, second)) \
                .all()

    @cache_result
    def get_pairs_with(self: Database, name: str) -> list[PairData]:
        """Get all pairings involving a specific person"""
        return SESSION.query(PairData) \
                .filter(PairData.member1 == name or PairData.member2 == name) \
                .all()
    
    @cache_result
    def get_all_pairs_involving(self: Database, names: list[str]) -> list[PairData]:
        """Get all pairs that only involve the names listed."""
        # I blame chatgpt when this breaks.
        subquery = (
            SESSION.query(
                PairData.member1,
                PairData.member2,
                func.max(PairData.last_date).label('max_last_date')
            )
            .group_by(PairData.member1, PairData.member2)
            .subquery()
        )

        query = (
            SESSION.query(PairData)
            .join(
                subquery,
                and_(
                    PairData.member1 == subquery.c.member1,
                    PairData.member2 == subquery.c.member2,
                    PairData.last_date == subquery.c.max_last_date
                )
            )
            .filter(
                PairData.member1.in_(names),
                PairData.member2.in_(names)
            )
        )

        return query.all()

    def close(save: bool = True):
        if save: SESSION.commit()
        SESSION.close()

    # Other stuff

    @cache_result
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
