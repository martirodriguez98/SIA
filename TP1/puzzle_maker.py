import random
import numpy as np

from TP1.state import State

BOARD_SIZE = 3
OBJECTIVE: State = State(
    np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]], int), [2, 2]
)


def create_puzzle(iterations: int) -> State:
    initial_state: State = OBJECTIVE
    state_chosen: State = initial_state
    for _ in range(iterations):
        possible_moves = state_chosen.get_valid_moves()
        move_chosen = random.choice(possible_moves)
        state_chosen = state_chosen.move_empty_box(move_chosen)
    return state_chosen
