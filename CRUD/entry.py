from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class Entry:
    """An entry in the Beanz Database, keyed by the IDs of two people."""


    last_meeting: date = date.min
    """When, if ever, these people met. 
    Defaults to year 1 (a very long time ago)"""
    dislike_AB: bool = False
    """Whether the first person does not want to match with the second."""
    dislike_BA: bool = False
    """Whether the second person does not want to match with the first."""

    def random_weight(self: Entry, now: date) -> float:
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
    
    def update_dislike(self: Entry, ab: bool, ba: bool) -> Entry:
        return Entry(last_meeting=self.last_meeting,
                     dislike_AB=ab, dislike_BA=ba)

    def update_last_meeting(self: Entry, recent_meeting: date):
        # Assuming that, if people meet, they don't dislike each other.
        return Entry(last_meeting=recent_meeting)