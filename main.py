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
    "Charlotte George",
    "Bonus guy"
]

db = load("testcat1.json")

all_pairs: set[tuple[str]] = set()
day = date.today() + timedelta(days=202)

print(pair_names(db, names, day))