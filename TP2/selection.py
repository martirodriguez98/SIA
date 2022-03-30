import math
import random
from typing import Dict, Tuple, Callable, Collection, List, Set

import numpy as np
from numpy.random.mtrand import choice
from schema import Schema, And, Or

from bag import Bag, Individual
from config_loader import Param, ParamValidator, Config
from generation import Generation, Population

Selector = Callable[[Generation, Bag, int], Population]
InternalSelector = Callable[[Generation, Bag, int, Param], Population]


def validate_selector_params(params: Param) -> Param:
    return Config.validate_param(params, Schema({
        'method': {
            'name': And(str, Or(*tuple(selector_function.keys()))),
        }
    }, ignore_extra_keys=True))


def get_selector(params: Param) -> Selector:
    validate_selector_params(params)
    method, selection_param_schema = selector_function[params['method']['name']]
    validated_params: Param
    try:
        validated_params = params['method']['params']
    except:
        validated_params = None
    if selection_param_schema:
        validated_params = Config.validate_param(validated_params, selection_param_schema)
    # validated_params: Param = (
    #     Config.validate_param(params, selection_param_schema) if selection_param_schema else params
    # )
    return lambda gen, bag, amount: method(gen, bag, amount, validated_params)


def get_individual_probs(population: Population, bag: Bag) -> Collection[float]:
    aux: List = []
    population_fit = bag.population_fitness(population)
    for i in range(len(population)):
        aux.append(bag.calculate_total_fitness(population[i]) / population_fit)
    return aux


def elite_selector(generation: Generation, bag: Bag, size: int, param: Param) -> Population:
    return sorted(generation.population, key=lambda i: bag.calculate_total_fitness(i), reverse=True)[0:size]


def roulette_random_number(population: Population, bag: Bag, size: int) -> Population:
    result = np.random.choice(len(population), size, p=get_individual_probs(population, bag))
    new_pop: Population = []
    for r in range(len(result)):
        new_pop.append(population[result[r]])
    return new_pop


def roulette_selector(generation: Generation, bag: Bag, size: int, param: Param) -> Population:
    return roulette_random_number(generation.population, bag, size)


def rank_selector(generation: Generation, bag: Bag, size: int, param: Param) -> Population:
    sorted_pop = sorted(generation.population, key=lambda ind: bag.calculate_total_fitness(ind), reverse=True)
    weights = []
    pop_size = len(generation.population)
    for i in range(pop_size):
        weights.append((pop_size - (i + 1)) / pop_size)
    return random.choices(population=sorted_pop, weights=weights, k=size)


def get_prob(prob_list: np.ndarray) -> Collection[float]:
    return np.cumsum(prob_list / prob_list.sum())


def calculate_boltzmann(generation: Generation, bag: Bag, k: float, t0: float, tc: float) -> Collection[float]:
    if tc >= t0:
        raise ValueError(f'Error in Boltzmann Selection Method')
    t: float = tc + (t0 - tc) * (math.e ** (-k * generation.gen_count))

    new_fitness = []
    total_fitness = 0
    for ind in generation.population:
        aux = bag.calculate_total_fitness(
            ind) / 100  # dividimos por 100 porque hay fitness que son muy grandes y la exponencial no da
        f = math.exp(aux / t)
        new_fitness.append(f)
        total_fitness += f

    for f in range(len(new_fitness)):
        new_fitness[f] = new_fitness[f] / total_fitness
    return new_fitness


def boltzmann_selector(generation: Generation, bag: Bag, size: int, param: Param) -> Population:
    result = choice(len(generation.population), size,
                    p=calculate_boltzmann(generation, bag, param['k'], param['initial_temp'], param['final_temp']))
    new_pop: Population = []
    for r in range(len(result)):
        new_pop.append(generation.population[result[r]])
    return new_pop


def probabilistic_selection(population: Population, bag: Bag, tournament_prob: float) -> Individual:
    rand: float = random.uniform(0, 1)
    fitness_1: float = bag.calculate_total_fitness(population[0])
    fitness_2: float = bag.calculate_total_fitness(population[1])
    if rand < tournament_prob:
        if fitness_1 > fitness_2:
            return population[0]
        else:
            return population[1]
    else:
        if fitness_1 < fitness_2:
            return population[0]
        else:
            return population[1]


def tournament_winner(population: Population, bag: Bag, tournament_prob: float) -> Individual:
    winners = [
        probabilistic_selection(random.sample(population, 2), bag, tournament_prob),
        probabilistic_selection(random.sample(population, 2), bag, tournament_prob)
    ]
    return probabilistic_selection(winners, bag, tournament_prob)


def prob_tournament_selector(generation: Generation, bag: Bag, size: int, param: Param) -> Population:
    winners: Set = set()
    while len(winners) < size:
        winners.add(tuple(tournament_winner(generation.population, bag, param['tournament_probability'])))
    return list(winners)


def truncate_selector(generation: Generation, bag: Bag, size: int, param: Param) -> Population:
    if param['k'] >= math.floor(size / 2):
        raise ValueError(f'Error in Truncate Selection Method.')
    new_pop = sorted(generation.population.copy(), key=lambda i: bag.calculate_total_fitness(i))
    new_pop = new_pop[param['k']:]
    return random.sample(new_pop, size)


# validators
boltzmann_validator: ParamValidator = Schema({
    'initial_temp': And(Or(float, int), lambda t0: t0 > 0),
    'final_temp': And(Or(float, int), lambda tc: tc > 0),
    'k': And(Or(float, int), lambda k: k > 0)
}, ignore_extra_keys=True)

prob_tournament_validator: ParamValidator = Schema({
    'tournament_probability': And(float, lambda p: 0.5 <= p <= 1)
}, ignore_extra_keys=True)

truncate_validator: ParamValidator = Schema({
    'k': And(int, lambda k: k > 0)
}, ignore_extra_keys=True)

selector_function: Dict[str, Tuple[InternalSelector, ParamValidator]] = {
    'elite': (elite_selector, None),
    'roulette': (roulette_selector, None),
    'rank': (rank_selector, None),
    'boltzmann': (boltzmann_selector, boltzmann_validator),
    'prob_tournament': (prob_tournament_selector, prob_tournament_validator),
    'truncate': (truncate_selector, truncate_validator)
}
