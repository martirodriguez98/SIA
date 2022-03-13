import sys
from time import perf_counter
from typing import Collection, Callable, Dict

import numpy as np

from config_loader import Config, StrategyParams
from puzzle_maker import create_puzzle
from state import State
from statistics import Statistics
from strategies.a_star import a_star
from strategies.bpp import bpp
from strategies.bpa import bpa
from strategies.bppv import bppv
from strategies.global_heuristic import global_heuristic
from strategies.local_heuristic import local_heuristic

strategy_map: Dict[str, Callable[[State, StrategyParams, Statistics], Collection[State]]] = {
    'BPA': bpa,  # BFS
    'BPP': bpp,  # DFS
    'BPPV': bppv,  # IDDFS
    'LOCAL_H': local_heuristic,
    'GLOBAL_H': global_heuristic,
    'A_STAR': a_star
}


def main(config_file: str):
    config: Config = Config(config_file)
    stats: Statistics = Statistics(config)

    if config.initial_puzzle is not None:
        index = np.where(config.initial_puzzle == 0)
        initial_puzzle: State = State(config.initial_puzzle, [index[0][0], index[1][0]])
    else:
        initial_puzzle: State = create_puzzle(100)

    states: Collection[State] = puzzle_solver(initial_puzzle, config.strategy, config.strategy_params, stats)
    stats.print_stats()
    print(f'Solution:\n')
    for s in states:
        print(s)


def puzzle_solver(initial_puzzle: State, strategy: str, strategy_params: StrategyParams, stats: Statistics) -> \
        Collection[State]:
    if strategy not in strategy_map:
        raise ValueError(f'Invalid strategy {strategy}. Valid strategies: {strategy_map.keys()}')

    start_time: float = perf_counter()
    states: Collection[State] = strategy_map[strategy](initial_puzzle, strategy_params, stats)
    end_time: float = perf_counter()
    stats.set_process_time(start_time, end_time)
    stats.set_depth(len(states))

    if not states:
        stats.set_border_nodes_count(0)
    else:
        stats.set_states(states)

    return states


if __name__ == "__main__":
    argv = sys.argv
    config_file: str = 'config.yaml'

    # if another file is provided
    if len(argv) > 1:
        config_file = argv[1]

    try:
        main(config_file)

    except ValueError as e:
        print(f'Error found in {config_file}\n{e}')

    except FileNotFoundError as e:
        print(f'Configuration file {e.filename} not found')

    except KeyboardInterrupt:
        print('Program was interrupted. Puzzle resolution ended incomplete.')
