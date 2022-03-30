import random
from random import random
from typing import Tuple
from bag import Individual
from generation import Population


def get_couples(parents: Population) -> Tuple[Individual, Individual]:
    couple = random.sample(parents, 2)
    return couple[0], couple[1]
