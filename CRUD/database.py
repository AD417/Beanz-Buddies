from __future__ import annotations

from CRUD.entry import Entry


class Database:
    """A basic CRUD system to store all pairing entries."""

    def __init__(self: Database, filepath: str | None = None) -> None:
        self._data: dict[tuple[str, str], Entry] = {}


    # CREATE

    def add_pair(self: Database, first: str, second: str):
        """Add a match pair to the database."""
        if first == second: return # No self-pairs

        if first < second:
            first, second = second, first # Sort lexicographically

        if (first, second) in self._data: return # No overwrites

        self._data[(first, second)] = Entry()

    def add_all_pairs(self: Database, names: list[str]):
        """Add all possible pairs given a list of names to the database."""
        for first in range(len(names)):
            for second in range(first+1, len(names)):
                self.add_pair(names[first], names[second])

    # READ

    def get_pair(self: Database, first: str, second: str) -> Entry:
        """Get the data for a specific pair from the database."""
        if first < second:
            first, second = second, first
        
        if (first, second) not in self._data:
            self.add_pair(first, second)

        return self._data[(first, second)]
    
    def get_all_pairs_with(self: Database, name: str):
        """Get all pairs involving some person. 
        Consider for a moment if you should instead use get_2D_map."""

        entries: list[Entry] = []

        for pair in self._data.keys():
            if pair[0] != name and pair[1] != name: continue
            entries += [self._data[pair]]
        
        return entries
    
    def get_2D_map(self: Database):
        """Get all pairs in a 2D map. 
        Instead of using `db.get_pair("Ada","Bobby")`, 
        you can use `map["Ada"]["Bobby"]`."""

        data: dict[str, dict[str, Entry]] = {}

        for pair in self._data.keys():
            first, second = pair

            if first not in data:
                data[first] = {}
            if second not in data:
                data[second] = {}

            data[first][second] = self._data[pair]
            data[second][first] = self._data[pair]

        return data

    # UPDATING

    def set_pair(self: Database, first: str, second: str, entry: Entry):
        if first < second: 
            first, second = second, first
        
        self._data[(first, second)] = entry
