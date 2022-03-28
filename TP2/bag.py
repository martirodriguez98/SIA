from typing import Set, List

import numpy as np

from data_loader import Item

Individual = List[int]
Population = List[Individual]


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

    # todo bajar fitness a individuos que se pasan del peso maximo
    def calculate_total_fitness(self, individual: Individual) -> float:
        total_fitness: float = 0
        index = 0
        for i, e in zip(individual, self.items):
            if i:
                total_fitness += e.fitness
            index += 1
        if self.calculate_weight(individual) > self.max_weight:
            total_fitness *= 0.3
        return total_fitness

    def population_fitness(self, population: Population):
        total_fitness: float = 0
        for i in range(len(population)):
            total_fitness += self.calculate_total_fitness(population[i])
        return total_fitness

    def best_fitness(self, population: Population):
        best_fitness: float = 0
        for i in range(len(population)):
            aux: float = self.calculate_total_fitness(population[i])
            if aux > best_fitness:
                best_fitness = aux
        return best_fitness

    def generate_random_set(self) -> Individual:
        current_weight = 0
        individual: Individual = []
        for i in range(self.max_items):
            individual.append(0)

        indexes: Individual = []
        for i in range(self.max_items):
            indexes.insert(i, i)

        while len(indexes) > 0:
            if len(indexes) != 1:
                index = np.random.randint(0, len(indexes) - 1)
            else:
                index = 0
            if current_weight + self.items[indexes[index]].weight <= self.max_weight:
                current_weight += self.items[indexes[index]].weight
                individual[indexes[index]] = 1
            indexes.pop(index)

        return individual
