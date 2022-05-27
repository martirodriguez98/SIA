import sys
from typing import Optional, Dict, Any

import schema
import yaml
from schema import Schema, SchemaError

Param = Optional[Dict[str, Any]]

class Config:

    @staticmethod
    def validate_param(param: Param, schema: Schema) -> Param:
        try:
            return schema.validate(param)
        except SchemaError as e:
            print('A problem was found on the configuration file:\n')
            sys.exit(e.code)

    def __init__(self, config_path: str):
        try:
            stream = open(config_path, 'r')
        except FileNotFoundError:
            raise ValueError(f'{config_path} Config file not found.')

        try:
            args = yaml.safe_load(stream)
        except Exception:
            raise ValueError(f'Invalid syntax in Config file {config_path}')

        args = Config.validate_param(args, Schema({
            'dataset': str,
            'k': schema.And(int, lambda k: k > 0),
            'learning_rate': schema.And(float, lambda learning_rate: 0 < learning_rate < 1)
        }))

        self.dataset: str = args['dataset']
        self.k: int = args['k']
        self.learning_rate: float = args['learning_rate']