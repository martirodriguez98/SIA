from random import random
from typing import Callable, Iterator, Dict, Optional, Tuple

import numpy as np
from schema import Schema, And, Or

from bag import Individual
from config_loader import Param, Config
from generation import Population

Crossover = Callable[[Individual,Individual],Tuple[Individual,Individual]]
MethodSelector = Callable[[Individual,Individual,Optional[int]], Tuple[Individual,Individual]]

def validate_params(params: Param) -> Param:
    return Config.validate_param(params, Schema({
        'method': {
            'name': And(str, Or(*tuple(crossing_function.keys())))
        }
    }, ignore_extra_keys=True))

def get_crossover(params: Param) -> Crossover:
    validate_params(params)
    method = crossing_function[params['method']['name']]
    return method

def get_single_point(first_parent: Individual, second_parent: Individual, points_q: Optional[int] = None) -> Tuple[Individual,Individual]:
    return get_multiple_point(first_parent,second_parent,1)

def get_multiple_point(first_parent: Individual, second_parent: Individual, points_q: Optional[int]) -> Tuple[Individual,Individual]:
    size = len(first_parent)
    first_child: Individual = []
    second_child: Individual = []
    p = sorted(np.random.sample(range(1,size),points_q))
    switches: int = 0
    for i in range(size):
        if switches < points_q and i == p[switches]:
            switches += 1
        if switches % 2 == 0:
            first_child[i] = first_parent[i]
            second_child[i] = second_parent[i]
        else:
            first_child[i] = second_parent[i]
            second_child[i] = first_parent[i]

    return first_child,second_child

def get_uniform(first_parent: Individual, second_parent: Individual, points_q: Optional[int] = None) -> Tuple[Individual,Individual]:
    size = len(first_parent)
    first_child: Individual = []
    second_child: Individual = []
    for i in range(size):
        p = np.random.uniform()
        if p < 0.5:
            first_child[i] = first_parent[i]
            second_child[i] = second_parent[i]
        else:
            first_child[i] = second_parent[i]
            second_child[i] = first_parent[i]

    return first_child, second_child


crossing_function: Dict[str, MethodSelector] = {
    'single_point': get_single_point,
    'multiple_point': get_multiple_point,
    'uniform': get_uniform
}