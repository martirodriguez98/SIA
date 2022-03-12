import sys
from time import perf_counter
from typing import Collection, Callable, Dict, List

from TP1.puzzle_maker import create_puzzle
from TP1.state import State
from TP1.strategies.bpp import bpp
from TP1.strategies.bpa import bpa
from TP1.strategies.bppv import bppv

# def main(config_file: str):
#     states:Collection[State] = puzzle_solver()

strategy_map: Dict[str, Callable[[State], Collection[State]]] = {
    'BPA': bpa,  # BFS
    'BPP': bpp,  # DFS
    'BPPV': bppv  # IDDFS
}


def main():
    initial_puzzle: State = create_puzzle(100)
    print(f'Puzzle to solve: {initial_puzzle}')
    states: Collection[State] = puzzle_solver(initial_puzzle, 'BPP')


def puzzle_solver(initial_puzzle: State, strategy: str) -> Collection[State]:
    if strategy not in strategy_map:
        raise ValueError(f'Invalid strategy {strategy}. Valid strategies: {strategy_map.keys()}')

    start_time: float = perf_counter()
    print(initial_puzzle.puzzle)
    states: Collection[State] = strategy_map[strategy](initial_puzzle)
    end_time: float = perf_counter()
    i = 0
    for s in states:
        i += 1
        print(f'pasos: {i}\n {s}')
    print(end_time)
    return states


if __name__ == "__main__":
    argv = sys.argv
    try:
        # main(config_file)
        main()

    except FileNotFoundError as e:
        print(f'Configuration file {e.filename} not found')
