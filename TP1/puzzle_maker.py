from typing import List

import numpy as np

from TP1.state import State


def create_puzzle() -> State:
    random_matrix_array: List[List[int]] = np.random.choice(9,size=(3,3),replace=False)
    empty_box_x: int = -1
    empty_box_y: int = -1

    for x in range(len(random_matrix_array)):
        for y in range(len(random_matrix_array[x])):
            if(random_matrix_array[x][y] == 0):
                empty_box_x = x
                empty_box_y = y

    if (empty_box_x == -1 or empty_box_y == -1):
        raise ValueError('Invalid puzzle')

    return State(random_matrix_array,empty_box_x,empty_box_y)

