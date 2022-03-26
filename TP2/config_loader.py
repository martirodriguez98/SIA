import sys
from typing import Any, Dict, Optional

import schema
import yaml
from schema import Schema, SchemaError

Param = Dict[str, Any]
ParamValidator = Optional[Schema]


class Config:

    @staticmethod
    def validate_param(param: Param, schema: Schema) -> Param:
        try:
            return schema.validate(param)
        except SchemaError as e:
            print('A problem was found on the configuration file:\n')
            sys.exit(e.code)

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

        args = Config.validate_param(args, Schema({
            'items_file': str,
            'population_size': schema.And(int, lambda population_size: population_size > 0),
            'selector': dict,
            'crossover': dict
        }))

        self.items_file: str = args['items_file']
        self.population_size: int = args['population_size']
        self.selector: Param = args['selector']
        self.crossover: Param = args['crossover']

