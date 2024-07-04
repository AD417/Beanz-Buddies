from CRUD.database import Database
from CRUD.saving import save, load

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

pprint(db.get_2D_map()["Ada"])

save(db, "testcat.json")

db2 = load("testcat.json")

print()
pprint(db.get_2D_map()["Ada"])