import sys
import typing
from typing import Dict, Any

import yaml
from schema import Schema, Optional, SchemaError, And

Param = Dict[str, Any]
ParamValidator = typing.Optional[Schema]

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
            stream = open(config_path,'r')
        except FileNotFoundError:
            raise FileNotFoundError(f'Config file missing. Make sure "{config_path}" is present')

        try:
            args = yaml.safe_load(stream)
        except Exception:
            raise ValueError(f'Invalid syntax in Config file {config_path}')

        args = Config.validate_param(args, Schema({
            Optional('training_set', default=dict): {
                Optional('x', default=None): str,
                Optional('y', default=None): str,
                Optional('x_line_count',default=1): And(int,lambda i: i > 0),
                Optional('y_line_count',default=1): And(int,lambda i: i > 0),
            },
            'network': dict,
        }, ignore_extra_keys=True))

        self.training_set: Param = args['training_set']
        self.network: Param = args['network']

