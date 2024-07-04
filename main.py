from CRUD.database import Database

db = Database()

names = [
    "Ada",
    "Bobby",
    "Chrissy",
    "Darwin",
    "Ella",
    "Fernando",
    "Gavin",
    "Heela",
    "Igor",
    "James"
]

db.add_all_pairs(names)

from pprint import pprint

pprint(db.get_2D_map())