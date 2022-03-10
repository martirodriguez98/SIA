from typing import List, Set, Tuple

import numpy as np

from TP1.state import State


def create_puzzle() -> State:

    list = np.random.choice(9, size=(9), replace=False)
    random_array: Tuple = tuple(list)
    empty_box: int = -1

    for x in range(len(random_array)):
        if random_array[x] == 0:
            empty_box = x
            break

    if empty_box == -1:
        raise ValueError('Invalid puzzle')

    return State(random_array, empty_box)
