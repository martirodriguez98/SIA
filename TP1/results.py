import csv

from typing import List, Optional

from puzzle_maker import create_puzzle
from puzzle_solver import puzzle_solver
from state import State
from stats import Stats

from config_loader import StrategyParams

header = ['strategy', 'heuristic', 'result', 'cost', 'depth', 'expanded nodes', 'border nodes', 'limit',
          'processing_time']


def csv_results(file: str, data: List[List[str]]):
    with open(file, 'a') as f:
        writer = csv.writer(f)
        # write the header
        if not f.tell():
            writer.writerow(header)

        # write the data
        writer.writerows(data)

        f.close()

def generate_results(initial_state: State, strategy_name: str, strategy_params: Optional[StrategyParams] = None):


    stats: Stats = Stats(strategy_name, strategy_params)

    data = []
    for i in range(20):
        puzzle_solver(initial_state, strategy_name, strategy_params, stats)

        data.append(
            [strategy_name, strategy_params['heuristic'] if strategy_params is not None and strategy_params['heuristic'] else "",
             stats.result, stats.cost, stats.depth, stats.expanded_nodes_count, stats.border_nodes_count,
             strategy_params['step'] if strategy_params is not None and strategy_params['step'] else "", stats.process_time])

    csv_results(f'{strategy_name}.csv', data)


if __name__ == "__main__":
    init_state = create_puzzle(100)
    generate_results(init_state, "BPA")
    generate_results(init_state,"BPP")
    generate_results(init_state,"BPPV",{"step":20,"heuristic":None})
    generate_results(init_state,"BPPV",{"step":50,"heuristic":None})
    generate_results(init_state,"BPPV",{"step":70,"heuristic":None})
    generate_results(init_state,"LOCAL_H",{"step":None,"heuristic":"manhattan_distance"})
    generate_results(init_state,"LOCAL_H",{"step":None,"heuristic":"hamming_distance"})
    generate_results(init_state,"LOCAL_H",{"step":None,"heuristic":"manhattan_hamming"})
    generate_results(init_state,"GLOBAL_H",{"step":None,"heuristic":"manhattan_distance"})
    generate_results(init_state,"GLOBAL_H",{"step":None,"heuristic":"hamming_distance"})
    generate_results(init_state,"GLOBAL_H",{"step":None,"heuristic":"manhattan_hamming"})
    generate_results(init_state,"A_STAR",{"step":None,"heuristic":"manhattan_distance"})
    generate_results(init_state,"A_STAR",{"step":None,"heuristic":"hamming_distance"})
    generate_results(init_state,"A_STAR",{"step":None,"heuristic":"manhattan_hamming"})
