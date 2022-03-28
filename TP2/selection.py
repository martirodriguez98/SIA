import math
import random
from typing import Dict, Tuple, Callable, Collection, List, Optional, Any

import numpy as np
import schema
from numpy.random.mtrand import choice
from schema import Schema, And, Or

from bag import Bag, Individual
from config_loader import Param, ParamValidator, Config
from generation import Generation, Population

Selector = Callable[[Generation, Bag, int], Population]
InternalSelector = Callable[[Generation, Bag, int, Param], Population]

def validate_selector_params(params: Param) -> Param:
    method_schema: Dict[Any, Any] = {
        'name': And(str, Or(*tuple(selector_function.keys()))),
        schema.Optional('params', default=None): dict,
    }
    return Config.validate_param(params, Schema({
        'method': method_schema
    },ignore_extra_keys=True))


def get_selector(params: Param) -> Selector:
    params = validate_selector_params(params)
    method, selection_param_schema = selector_function[params['method']['name']]
    validated_params: Param = (
        Config.validate_param(params, selection_param_schema) if selection_param_schema else params
    )
    return lambda gen, bag, amount: method(gen, bag, amount,validated_params)


def get_individual_probs(population: Population, bag: Bag) -> Collection[float]:
    aux: List = []
    population_fit = bag.population_fitness(population)
    for i in range(len(population)):
        aux.append(bag.calculate_total_fitness(population[i]) / population_fit)
    return aux


def elite_selector(generation: Generation, bag: Bag, size: int, param: Param) -> Population:
    return sorted(generation.population, key=lambda i: bag.calculate_total_fitness(i), reverse=True)

def roulette_random_number(population: Population, bag: Bag, size: int) -> Population:
    result = np.random.choice(len(population), size, p=get_individual_probs(population, bag))
    new_pop: Population = []
    for r in range(len(result)):
        new_pop.append(population[result[r]])
    return new_pop

def roulette_selector(generation: Generation, bag: Bag, size: int, param: Param) -> Population:
    return roulette_random_number(generation.population, bag, size)

def rank_selector(generation: Generation, bag: Bag, size: int, param: Param) -> Population:
    sorted_pop = sorted(generation.population, key=lambda ind: bag.calculate_total_fitness(ind),reverse=True)
    weights = []
    for i in range(size):
        weights.append((size - (i+1)) / size)
    return random.choices(population=sorted_pop, weights=weights,k=size)

def get_prob(prob_list: np.ndarray) -> Collection[float]:
    return np.cumsum(prob_list / prob_list.sum())


def calculate_boltzmann(generation: Generation, bag: Bag, k: float, t0: float, tc: float) -> Collection[float]:
    if tc >= t0:
        raise ValueError(f'Error in Boltzmann Selection Method')
    t: float = tc + (t0 - tc) * math.exp(-k * generation.gen_count)
    fitness_list: np.ndarray = np.fromiter(
        map(lambda i: math.exp(bag.calculate_total_fitness(i) / t), generation.population), float)
    mean = np.mean(fitness_list)
    boltzmann_fitness_list = fitness_list / mean
    return get_prob(boltzmann_fitness_list)


def boltzmann_selector(generation: Generation, bag: Bag, size: int, param: Param) -> Population:
    return choice(generation.population, size, p=calculate_boltzmann(generation, bag, param['k'], param['initial_temp'], param['final_temp']))

def fitness_key(i: Individual, bag: Bag) -> float:
    return bag.calculate_total_fitness(i)

def probabilistic_selection(population: Population,bag: Bag, tournament_prob: float) -> Individual:
    rand: float = random.uniform(0,1)
    if rand < tournament_prob:
        return max(population, key=fitness_key) #TODO check if it's working
    else:
        return min(population, key=fitness_key)

def tournament_winner(population: Population,bag: Bag, tournament_prob: float) -> Individual:
    winners = [
        probabilistic_selection(random.sample(population,2),bag,tournament_prob),
        probabilistic_selection(random.sample(population,2),bag,tournament_prob)
    ]
    return probabilistic_selection(winners,bag,tournament_prob)

def prob_tournament_selector(generation: Generation, bag: Bag, size: int, param: Param) -> Population:
    return [
        tournament_winner(generation.population,bag,param['tournament_probability'])
        for _ in range(size)
    ]


def truncate_selector(generation: Generation, bag: Bag, size: int, param: Param) -> Population:
    if param['k'] >= math.floor(param['population_size']/2):
        raise ValueError(f'Error in Truncate Selection Method.')
    new_pop: Population = generation.population.copy()
    sorted(new_pop, key=lambda i: i.calculate_total_fitness(i))
    new_pop = new_pop[param['k']:]
    return choice(new_pop, size)

# validators
boltzmann_validator: ParamValidator = Schema({
    'initial_temp': And(Or(float,int), lambda t0: t0 > 0),
    'final_temp': And(Or(float,int), lambda tc: tc > 0),
    'k': And(Or(float,int), lambda k: k > 0)
}, ignore_extra_keys=True)

prob_tournament_validator: ParamValidator = Schema({
    'tournament_probability': And(float, lambda p: 0.5 <= p <= 1)
}, ignore_extra_keys=True)

truncate_validator: ParamValidator = Schema({
    'k': And(float, lambda k: k > 0)
}, ignore_extra_keys=True)

selector_function: Dict[str, Tuple[InternalSelector, ParamValidator]] = {
    'elite': (elite_selector, None),
    'roulette': (roulette_selector, None),
    'rank': (rank_selector, None),
    'boltzmann': (boltzmann_selector, boltzmann_validator),
    'prob_tournament': (prob_tournament_selector, prob_tournament_validator),
    'truncate': (truncate_selector, truncate_validator)
}

