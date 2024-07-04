from datetime import date
from functools import reduce
from CRUD.database import Database
from CRUD.entry import Entry

import random


def single_pairing(db: Database, names: list[str], now: date) -> list[tuple[str]]:
    pairs = []
    while len(names) >= 2:
        first = random.choice(names)
        names.remove(first)
        weights = [db.pair_weight(first, second, now) for second in names]

        second = random.choices(names, weights, k=1)[0]
        pairs += [(first, second)]
        names.remove(second)
    
    return pairs

def pairing_score(db: Database, pairs: list[tuple[str]], now: date) -> float:
    """
    Generate a "score" for a pairing, based on how well all the pairs
    coexist and don't result in recent pair repeats.
    This is a value between 0 and 1; it may be extremely small. 
    """
    return reduce(lambda x, y: x * db.pair_weight(y[0], y[1], now), pairs, 1)

def pair(db: Database, names: list[str], now: date, trials: int = 100):
    """
    Use a Monte Carlo simulation to generate a "good" pairing of
    all involved names. 
    """
    best_pairs = []
    best_score = -1

    # TODO: A random-choice gradient descent algorithm might work better here.
    # It would still need multiple trials, but would make good pairings better.
    for _ in range(trials):
        pairs = single_pairing(db, names, now)
        score = pairing_score(db, pairs, now)

        if score <= best_score: continue
        best_score = score
        best_pairs = pairs

    return best_pairs