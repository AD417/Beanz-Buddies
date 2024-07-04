from datetime import datetime
import json

from CRUD.database import Database
from CRUD.entry import Entry

def load(filepath: str) -> Database:
    with open(filepath, "r") as f:
        data = json.load(f)

    db = Database()
    for key in data:
        entry = data[key]
        entry["last_meeting"] = datetime.strptime(entry["last_meeting"], "%Y-%m-%d").date()
        entry = Entry(**entry)
        first, second = key.split("\t")
        db.set_pair(first, second, entry)

    return db

def save(db: Database, filepath: str):
    data = {}
    for pair in db:
        first, second = pair
        data[f"{first}\t{second}"] = db.get_pair(first, second).to_dict()
    
    with open(filepath, "w") as f:
        json.dump(data, f)