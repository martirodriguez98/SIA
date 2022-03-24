from typing import List

import bag
from bag import Bag

Population = List[bag.Individual]


class Generation:

    @staticmethod
    def create_first_generation(bag: Bag, generation_size: int) -> 'Generation':
        population: Population = []
        for _ in range(generation_size):
            population.append(bag.generate_random_set())
        return Generation(population, 0)

    def __init__(self, population: Population, gen_count: int):
        self.population: Population = population
        self.gen_count: int = gen_count
