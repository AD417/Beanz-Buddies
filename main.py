from datetime import date
from CRUD import *

db = Database()

names = [
    "Ada",
    "Bobby",
    "Chrissy",
    "Darwin",
    "Ella",
    "Frank",
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
for p in pair(db2, names, date.today()):
    print(p)
