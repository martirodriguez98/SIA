from typing import Optional, Dict, Any

import yaml

StrategyParams = Optional[Dict[str, Any]]


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
        self.strategy_params: StrategyParams = args['strategy'].get('params', None)

        return
