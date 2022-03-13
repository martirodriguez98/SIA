from typing import Callable, Dict

import numpy as np

from TP1.config_loader import StrategyParams
from TP1.state import State

OBJECTIVE: np.array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]], int)


def get_coordinate(num: int) -> [int, int]:
    index = np.where(OBJECTIVE == num)
    return [index[0][0], index[1][0]]


def hamming_distance(state: State) -> int:
    pieces: int = 0
    for x in range(len(state.puzzle)):
        for y in range(len(state.puzzle)):
            if state.puzzle[x][y] != (3 * x + y + 1) and state.puzzle[x][y] != 0:
                pieces = pieces + 1
    return pieces


def manhattan_distance(state: State) -> int:
    dist: int = 0
    for x in range(len(state.puzzle)):
        for y in range(len(state.puzzle)):
            coord = get_coordinate(state.puzzle[x][y])
            dist += (abs(x - coord[0]) + abs(y - coord[1]))
    return dist


def manhattan_hamming(state: State) -> int:
    return hamming_distance(state) + manhattan_distance(state)


heuristics: Dict[str, Callable[[State], int]] = {
    'hamming_distance': hamming_distance,
    'manhattan_distance': manhattan_distance,
    'manhattan_hamming': manhattan_hamming
}


def get_heuristic(heuristic_name: str) -> Callable[[State], int]:
    if heuristic_name not in heuristics:
        raise ValueError(f'Invalid heuristic {heuristic_name}. Currently supported: {heuristics.keys()}')
    return heuristics[heuristic_name]


def get_heuristic_from_params(params: StrategyParams) -> Callable[[State], int]:
    if not params or 'heuristic' not in params:
        raise ValueError(f'Invalid heuristic {params}. Currently supported: {heuristics.keys()}')
    return get_heuristic(params['heuristic'])
