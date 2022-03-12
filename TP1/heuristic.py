from typing import Callable, Dict

from TP1.config_loader import StrategyParams
from TP1.state import State


def pieces_out_of_place(state: State) -> int:
    pieces: int = 0
    for x in range(len(state.puzzle)):
        for y in range(len(state.puzzle)):
            if state.puzzle[x][y] != (3 * x + y + 1) and state.puzzle[x][y] != 0:
                pieces = pieces+1
    return pieces


heuristics: Dict[str, Callable[[State], int]] = {
    'pieces_out_of_place': pieces_out_of_place
}


def get_heuristic(heuristic_name: str) -> Callable[[State], int]:
    if heuristic_name not in heuristics:
        raise ValueError(f'Invalid heuristic {heuristic_name}. Currently supported: {heuristics.keys()}')
    return heuristics[heuristic_name]


def get_heuristic_from_params(params: StrategyParams) -> Callable[[State], int]:
    if not params or 'heuristic' not in params:
        raise ValueError(f'Invalid heuristic {params}. Currently supported: {heuristics.keys()}')
    return get_heuristic(params['heuristic'])
