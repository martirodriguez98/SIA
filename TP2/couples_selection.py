from random import random
from typing import Tuple

from bag import Individual
from generation import Population

Couple = Tuple[Individual, Individual]

def get_couples(parents: Population) -> Couple:
    couple = random.sample(parents,2)
    return couple[0], couple[1]