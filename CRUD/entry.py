from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class Entry:
    """An entry in the Beanz Database, keyed by the IDs of two people."""


    last_meeting: date = date.min
    """When, if ever, these people met. 
    Defaults to year 1 (a very long time ago)"""

    met: bool = False

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

    def update_last_meeting(self: Entry, recent_meeting: date, met: bool):
        # Technically, this just overwrites the entry. There may be more stuff to add.
        return Entry(last_meeting=recent_meeting, met=met)
    
    def to_dict(self: Entry) -> dict[str, str]:
        return {
            "last_meeting": str(self.last_meeting),
            "met": str(self.met)
        }