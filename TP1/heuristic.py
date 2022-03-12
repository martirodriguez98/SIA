from typing import Callable, Dict

from TP1.state import State


def pieces_out_of_place(state: State) -> int:
    print('pieces')
    return 1


heuristics: Dict[str, Callable[[State], int]] = {
    'pieces_out_of_place': pieces_out_of_place
}


def get_heuristic(heuristic_name: str) -> Callable[[State], int]:
    if heuristic_name not in heuristics:
        raise ValueError(f'Invalid heuristic {heuristic_name}. Currently supported: {heuristics.keys()}')
    return heuristics[heuristic_name]
