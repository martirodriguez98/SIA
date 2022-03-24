from typing import Dict, Tuple, Callable

from bag import Bag
from config_loader import Param, ParamValidator
from generation import Generation

Selector = Callable[[Generation, int],Bag]
InternalSelector = Callable[[Generation, Param], Bag]


def elite_selector(generation: Generation):
    return


def roulette_selector(generation: Generation):
    return


def rank_selector(generation: Generation):
    return


def boltzmann_selector(generation: Generation):
    return


def prob_tournament_selector(generation: Generation):
    return


def truncate_selector(generation: Generation):
    return


# TODO completar parámetros de las funciones
selector_function: Dict[str, Tuple[InternalSelector, ParamValidator]] = {
    'elite': (elite_selector, None),
    'roulette': (roulette_selector, None),
    'rank': (rank_selector, None),
    'boltzmann': (boltzmann_selector, None),
    'prob_tournament': (prob_tournament_selector, None),
    'truncate': (truncate_selector, None)
}
