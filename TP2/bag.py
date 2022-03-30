from typing import List

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

    def calculate_total_fitness(self, individual: Individual) -> float:
        weight = 0
        benefit = 0
        for i, e in zip(individual, self.items):
            if i:
                weight += e.weight
                benefit += e.benefit
        if weight > self.max_weight:
            weight = weight * (weight - self.max_weight)
            return benefit / weight
        return benefit

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
