import math
import random
from typing import Dict, Tuple, Callable, Collection, List

import numpy as np
from numpy.random.mtrand import choice

from bag import Bag
from config_loader import Param, ParamValidator
from generation import Generation, Population

Selector = Callable[[Generation, Bag], Population]
InternalSelector = Callable[[Generation, Param], Population]


def get_individual_probs(population: Population, bag: Bag) -> Collection[float]:
    aux: List = []
    population_fit = bag.population_fitness(population)
    for i in population:
        aux.append(bag.calculate_total_fitness(i) / population_fit)
    return aux


def roulette_random_number(population: Population, bag: Bag, size: int) -> Collection[float]:
    return choice(population, size, p=get_individual_probs(population, bag))


def elite_selector(generation: Generation) -> Population:
    return sorted(generation.population, key=lambda i: i.calculate_total_fitness(i), reverse=True)


def roulette_selector(generation: Generation, bag: Bag, size: int):
    return [
        roulette_random_number(generation.population, bag, size)
        for _ in range(size)
    ]


def rank_selector(generation: Generation):
    return


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


def boltzmann_selector(generation: Generation, bag: Bag, size: int, param: Param):
    return roulette_selector(
        generation,
        bag,
        roulette_random_number(generation.population, bag, size),
        calculate_boltzmann(generation, bag, param['k'], param['initial_temp'], param['final_temp'])
    )


def prob_tournament_selector(generation: Generation):
    return


def truncate_selector(generation: Generation):
    return


# TODO completar parámetros de las funciones
selector_function: Dict[str, Tuple[InternalSelector, ParamValidator]] = {
    'elite': (elite_selector, None),
    'roulette': (roulette_selector, None),
    'rank': (rank_selector, None),
    'boltzmann': (boltzmann_selector, None),  # TODO validador
    'prob_tournament': (prob_tournament_selector, None),
    'truncate': (truncate_selector, None)
}
