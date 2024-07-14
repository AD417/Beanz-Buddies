from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from functools import reduce
from CRUD.database import Database

import random

class Pairing(list):
    ...

@dataclass(frozen=True)
class PairingGenerator:
    FROSH_PENALTY = 0.1
    ALUMNI_PENALTY = 0.25

    # Maybe I don't need a class, but the number of relevant properties
    #  Made this seem like a good idea.
    frosh: set[str]
    active: set[str]
    alumni: set[str]
    db: Database
    now: date = date.today()

    @property
    def everyone(self) -> list[str]:
        return list(set.union(self.frosh, self.active, self.alumni))
    
    def best_possible_score(self) -> float:
        # Frosh without pairs
        unpaired = len(self.frosh) - len(self.active)
        if unpaired > 0:
            # Frosh left -- pair with alumni. 
            unpaired -= len(self.alumni)
            if unpaired >= 0:
                # Frosh still left...
                return PairingGenerator.FROSH_PENALTY ** (unpaired / 2)
            # Alumni left now
            return PairingGenerator.ALUMNI_PENALTY ** (-unpaired / 2)
        else:
            # Upperclassmen left -- pair with alumni
            unpaired = -unpaired
            unpaired -= len(self.alumni)
            if unpaired >= 0:
                # Upperclassmen pair with themselves.
                return 1
            # Alumni left now.
            return PairingGenerator.ALUMNI_PENALTY ** (-unpaired / 2)

    def make_pairing(self) -> Pairing:
        names = self.everyone
        pairs = Pairing()
        while len(names) >= 2:
            first = random.choice(names)
            names.remove(first)
            weights = [self.db.pair_weight(first, second, self.now) for second in names]

            if sum(weights) == 0:
                # We dun goofd
                second = names[0]
            else:
                second = random.choices(names, weights, k=1)[0]
            
            pairs += [(first, second)]
            names.remove(second)
        
        return pairs
    
    def single_pair_score(self, pair: tuple[str]) -> float:
        p1, p2 = pair
        base_score = 1.0
        if p1 in self.frosh and p2 in self.frosh:
            base_score = PairingGenerator.FROSH_PENALTY
        if p1 in self.alumni and p2 in self.alumni:
            base_score = PairingGenerator.ALUMNI_PENALTY
        
        return base_score * self.db.pair_weight(p1, p2, self.now)


    def score_pairing(self, pairs: Pairing) -> float:
        score = 1.0
        for pair in pairs:
            score *= self.single_pair_score(pair)
        
        return score
    
    def is_good_swap(self, pair1, pair2) -> bool:
        unique_names = set()
        unique_names.update(pair1, pair2)
        if len(unique_names) != 4: return False

        score_now = self.single_pair_score(pair1) * self.single_pair_score(pair2)
        next1 = (pair1[0], pair2[0])
        next2 = (pair1[1], pair2[1])
        score_next = self.single_pair_score(next1) * self.single_pair_score(next2)

        return score_next > score_now
    
    def make_good_pairing(self, trials: int = 1000, swaps_per: int = 1000):
        best_pairing: Pairing = None
        best_score = -1
        max_score = self.best_possible_score()

        def make_optimized_pair():
            pairs = self.make_pairing()

            indices = [x for x in range(len(pairs))]

            for _ in range(swaps_per):
                # Randomly pick 2 pairs.
                i1, i2 = random.sample(indices, k=2)
                pair1 = pairs[i1]
                pair2 = pairs[i2]
                # Does swapping them improve the results, however marginally?
                if not self.is_good_swap(pair1, pair2): continue
                # If so, do it. 
                next1, next2 = [*zip(pair1, pair2)]
                pairs[i1] = next1
                pairs[i2] = next2
            
            return pairs
        
        with ThreadPoolExecutor() as executor:
            pair_makers = [executor.submit(make_optimized_pair) for _ in range(trials)]

            for future in as_completed(pair_makers):
                pairs = future.result()

                score = self.score_pairing(pairs)
                print(score)

                if score <= best_score: continue
                best_score = score
                best_pairing = pairs

                if best_score >= max_score: return best_pairing

        return best_pairing#