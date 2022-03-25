from typing import Set, List

import numpy as np

from data_loader import Item
from generation import Population

Individual = List[int]


class Bag:
    def __init__(self, max_items: int, max_weight: int, items: List[Item]):
        self.items: List[Item] = items
        self.max_weight: int = max_weight
        self.max_items: int = max_items
        self.weight: int = 0
        self.benefit: int = 0

    def calculate_weight(self, individual: Individual) -> int:
        total_weight: int = 0
        for i, e in zip(individual, self.items):
            if i:
                total_weight += e.weight
        return total_weight

    def calculate_benefit(self, individual: Individual) -> int:
        total_benefit: int = 0
        for i, e in zip(individual, self.items):
            if i:
                total_benefit += e.benefit
        return total_benefit

    def calculate_total_fitness(self, individual: Individual) -> float:
        total_fitness: int = 0
        for i, e in zip(individual, self.items):
            if i:
                total_fitness += e.fitness
        return total_fitness

    def population_fitness(self, population: Population):
        total_fitness: int = 0
        for i in population:
            total_fitness += self.calculate_total_fitness(i)
        return total_fitness

    def generate_random_set(self) -> Individual:
        current_weight = 0
        individual: Individual = []
        for i in range(self.max_items):
            individual.append(0)

        count: int = self.max_items

        while current_weight <= self.max_weight and count > 0:
            index = np.random.randint(0, len(self.items))
            count -= 1
            if individual[index] != 1:
                if current_weight + self.items[index].weight <= self.max_weight:
                    current_weight += self.items[index].weight
                    individual.insert(index, 1)
        return individual
