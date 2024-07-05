from datetime import date
from CRUD import *

from datetime import datetime

start = datetime.now()

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
]

print(names)

db.add_pair("Liriel Bryer", "Emily Caston")

pairs = generate_pairs(db, names, date.today())

for pair in pairs: 
    print(pair)
    db.add_pair(*pair)

db.close()

end = datetime.now()

print(f"This took {end - start} seconds, by the way.")