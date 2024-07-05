from datetime import date
from functools import reduce
from CRUD.database import Database

import random


def single_pairing(db: Database, names: list[str], now: date) -> list[tuple[str]]:
    pairs = []
    while len(names) >= 2:
        first = random.choice(names)
        names.remove(first)
        weights = [db.pair_weight(first, second, now) for second in names]

        if sum(weights) == 0:
            # We dun goofd
            second = names[0]
        else:
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

def is_good_swap(db: Database, pair1: tuple[str], pair2: tuple[str], now: date) -> bool:
    unique_names = set()
    unique_names.update(pair1, pair2)
    if len(unique_names) != 4: return False
    score_now = db.pair_weight(pair1[0], pair1[1], now) * db.pair_weight(pair2[0], pair2[1], now)
    score_next = db.pair_weight(pair1[0], pair2[0], now) * db.pair_weight(pair1[1], pair2[1], now)

    return score_next > score_now

def generate_pairs(db: Database, names: list[str], now: date, trials: int = 1, swaps: int = 0):
    """
    Use a Monte Carlo simulation to generate a "good" pairing of
    all involved names. 
    """
    best_pairs = []
    best_score = -1

    for _ in range(trials):
        pairs = single_pairing(db, names.copy(), now)

        for _ in range(swaps):
            # Randomly pick 2 pairs.
            pair1, pair2 = random.choices(pairs, k=2)
            # Does swapping them improve the results, however marginally?
            if not is_good_swap(db, pair1, pair2, now): continue
            # If so, do it. 
            # TODO: use a set instead of a list.
            pairs.remove(pair1)
            pairs.remove(pair2)
            pairs += [*zip(pair1, pair2)]


        score = pairing_score(db, pairs, now)

        if score <= best_score: continue
        best_score = score
        best_pairs = pairs

    print(best_score)
    return best_pairs#