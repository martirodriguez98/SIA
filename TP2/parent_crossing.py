from random import sample
from typing import Callable, Iterator, Dict, Optional, Tuple

import numpy as np
import schema
from schema import Schema, And, Or

from bag import Individual
from config_loader import Param, Config, ParamValidator
from generation import Population

Crossover = Callable[[Individual,Individual],Tuple[Individual,Individual]]
MethodSelector = Callable[[Individual,Individual,Param], Tuple[Individual,Individual]]

def validate_params(params: Param) -> Param:
    return Config.validate_param(params, Schema({
        'method': {
            'name': And(str, Or(*tuple(crossing_function.keys())))
        }
    }, ignore_extra_keys=True))

def get_crossover(params: Param) -> Crossover:
    validate_params(params)
    method, crossover_params_schema = crossing_function[params['method']['name']]
    crossover_params: Param = params['method']['params']
    if crossover_params_schema:
        crossover_params = Config.validate_param(crossover_params,crossover_params_schema)
    return lambda first, second: method(first,second,crossover_params)

def get_single_point(first_parent: Individual, second_parent: Individual, param: Param) -> Tuple[Individual,Individual]:
    return aux_get_multiple_point(first_parent,second_parent,1)

def get_multiple_point(first_parent: Individual, second_parent: Individual, param: Param) -> Tuple[Individual,Individual]:
    return aux_get_multiple_point(first_parent,second_parent,param['points_q'])

def aux_get_multiple_point(first_parent: Individual, second_parent: Individual,points_q: int) -> Tuple[Individual,Individual]:
    size = len(first_parent)
    first_child: Individual = []
    second_child: Individual = []
    if points_q > size:
        raise ValueError('Error in get multiple point function. Points_q must be lower than population size')
    p = sample(range(1,len(first_parent) - 1),points_q)
    p.sort()

    switches: int = 0
    for i in range(size):
        if switches < points_q and i == p[switches]:
            switches += 1
        if switches % 2 == 0:
            first_child.insert(i,first_parent[i])
            second_child.insert(i,second_parent[i])
        else:
            first_child.insert(i,second_parent[i])
            second_child.insert(i, first_parent[i])
    return first_child,second_child

def get_uniform(first_parent: Individual, second_parent: Individual, param: Param) -> Tuple[Individual,Individual]:
    size = len(first_parent)
    first_child: Individual = []
    second_child: Individual = []
    for i in range(size):
        p = np.random.uniform()
        if p < 0.5:
            first_child.insert(i,first_parent[i])
            second_child.insert(i,second_parent[i])
        else:
            first_child.insert(i,second_parent[i])
            second_child.insert(i, first_parent[i])

    return first_child, second_child

multiple_point_schema: ParamValidator = Schema({
    schema.Optional('points_q',default=2): And(int, lambda p: p > 1)
}, ignore_extra_keys=True)

crossing_function: Dict[str, Tuple[MethodSelector, ParamValidator]] = {
    'single_point': (get_single_point, None),
    'multiple_point': (get_multiple_point, multiple_point_schema),
    'uniform': (get_uniform, None)
}