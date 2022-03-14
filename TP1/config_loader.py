from typing import Optional, Dict, Any, List

import numpy as np
import yaml

StrategyParams = Optional[Dict[str, Any]]
BOARD_SIZE = 3


class Config:
    def __init__(self, config_path: str):
        # if a different path is receive for configuration we have to open it and set it
        try:
            stream = open(config_path, 'r')
        except FileNotFoundError:
            raise ValueError(f'{config_path} Config file not found.')

        try:
            args = yaml.safe_load(stream)
        except Exception:
            raise ValueError(f'Invalid syntax in Config file {config_path}')

        if 'strategy' not in args or 'name' not in args['strategy']:
            raise ValueError('Missing values. "strategy: name" must be present')

        self.strategy: str = args['strategy']['name']

        if self.strategy in ["LOCAL_H", "GLOBAL_H", "A_STAR"]:
            if 'params' not in args['strategy']:
                raise ValueError('Missing values. "strategy: params" must be present')
            if args['strategy']['params'] is None:
                raise ValueError('Missing values. "params: heuristic" must be present')

        self.strategy_params: StrategyParams = args['strategy'].get('params', None)

        puzzle_str: str = args.get('initial_puzzle', None)
        self.initial_puzzle: Optional[np.array] = None
        if puzzle_str is not None:
            self.initial_puzzle = np.array((args.get('initial_puzzle')), int)


        # check if matrix provided is ok

        if self.initial_puzzle is not None:
            if type(self.initial_puzzle) != np.ndarray or self.initial_puzzle.size != 9:
                raise ValueError(f'Invalid syntax in Config file {config_path}. Initial puzzle must be a matrix of size 3.')

        puzzle_as_list: List[int] = []
        if self.initial_puzzle is not None:
            if len(self.initial_puzzle) != BOARD_SIZE:
                raise ValueError(f'Invalid syntax in Config file {config_path}. Matrix must be of size {BOARD_SIZE}.')
            for x in range(len(self.initial_puzzle)):
                for y in range(len(self.initial_puzzle)):
                    if len(self.initial_puzzle[x]) != BOARD_SIZE:
                        raise ValueError(
                            f'Invalid syntax in Config file {config_path}. Matrix must be of size {BOARD_SIZE}.')
                    puzzle_as_list.append(self.initial_puzzle[x][y])
                    if self.initial_puzzle[x][y] < 0 or self.initial_puzzle[x][y] > 8:
                        raise ValueError(
                            f'Invalid syntax in Config file {config_path}. Elements in matrix must be from 0 to 8.')

        if len(puzzle_as_list) != len(set(puzzle_as_list)):
            raise ValueError(f'Invalid syntax in Config file {config_path}. Elements in matrix cant be repeated.')

        return

    def __repr__(self):
        return f'Strategy: {repr(self.strategy)}\n Strategy parameters: {repr(self.strategy_params)}\n'
