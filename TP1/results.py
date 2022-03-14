import csv
import yaml
from typing import List

from puzzle_maker import create_puzzle
from puzzle_solver import puzzle_solver
from statistics import Statistics
from config_loader import Config

header = ['strategy', 'heuristic', 'result', 'cost', 'depth', 'expanded nodes', 'border nodes', 'limit',
          'processing_time']


def csv_results(file: str, data: List[List[str]]):
    with open(file, 'w') as f:
        writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerow(data)


def generate_results(initial_state: str, strategy_name: str, heuristic=None, step=None):

    result = {
        'initial_puzzle': initial_state,
        'strategy': {
            'name': strategy_name,
        }
    }

    if heuristic is not None:
        result = {
            'initial_puzzle': initial_state,
            'strategy': {
                'name': strategy_name,
                'params': {
                    'heuristic': heuristic
                }
            }
        }

    if step is not None:
        result = {
            'initial_puzzle': initial_state,
            'strategy': {
                'name': strategy_name,
                'params': {
                    'step': step
                }
            }
        }



    with open('config.yaml', 'w') as file:
        document = yaml.dump(result, file)

    config = Config('config.yaml')

    stats: Statistics = Statistics(config)

    data = []
    for i in range(20):
        puzzle_solver(config.initial_puzzle, config.strategy, config.strategy_params, stats)
        data.append(
            [config.strategy, config.strategy_params['heuristic'] if config.strategy_params['heuristic'] else "",
             stats.result, stats.cost, stats.depth, stats.expanded_nodes_count, stats.border_nodes_count,
             config.strategy_params['step'] if config.strategy_params['step'] else "", stats.process_time])

    csv_results(f'{strategy_name}.csv', data)


if __name__ == "__main__":
    init_state = create_puzzle(100)
    state_str = (",".join(str(init_state.puzzle).splitlines()))
    state_str = state_str.replace(' ',',')
    state_str = state_str.replace(',,',',')
    state_str = state_str.replace('\'','')
    print(state_str)
    generate_results(state_str, "BPA")
