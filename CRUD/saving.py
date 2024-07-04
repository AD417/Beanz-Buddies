import json

from CRUD.database import Database
from CRUD.entry import Entry

def load(filepath: str) -> Database:
    with open(filepath, "r") as f:
        data = json.load(f)

    db = Database()
    for key in data:
        entry = Entry(**data[key])
        first, second = key.split("\t")
        db.set_pair(first, second, entry)

    return db

def save(db: Database, filepath: str):
    data = {}
    for pair in db._data:
        first, second = pair
        data[f"{first}\t{second}"] = db._data[pair].to_dict()
    
    with open(filepath, "w") as f:
        json.dump(data, f)