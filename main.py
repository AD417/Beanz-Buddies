from datetime import date, timedelta
from CRUD import *

db = Database()

names = [
    "Benjamin Piro",
    "Katie Koontz",
    "Nidhi Baindur",
    "Joe Abbate",
    "Dani Saba",
    "Joe Vita",
    "Chrissy Espeleta",
    "Connor Langa",
    "Zachary Cox",
    "Ian Kopke",
    "Sam Cordry",
    "Grant Hawerlander",
    "Eva",
    "Ekam",
    "Ethan Ferguson",
    "Mary Strodl",
    "Vivian Hafener",
    "Mirai Day",
    "Asha Kadagala",
    "Emma Schmidt",
    "Gavin McConnell",
    "Jason Koser",
    "Jinna Smail",
    "Joseph Issac",
    "Matt Marafino",
    "Will Hellinger",
    "Wilson McDade",
    "Adam Newlight",
    "Darwin Tran",
    "Tyler Samay",
    "Ella Soccoli",
    "Charlotte George"
]

# db.add_all_pairs(names)

all_pairs: set[tuple[str]] = set()
day = date.today()
delta = timedelta(days=2)

for i in range(100):
    pairs = pair_names(db, names, day)

    for p in pairs:
        all_pairs.add(p)
        first, second = p
        db.set_pair_date(first, second, day)

    print(pairs)
    day += delta

save(db, "testcat.json")