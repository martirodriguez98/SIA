from typing import Set, Tuple, List

import numpy as np

import bag
from bag import Bag
from config_loader import Config
from data_loader import Item
from generation import Generation, Population
from mutation import mutate
from parent_crossing import get_crossover, Crossover
from selection import Selector, get_selector


class Resolver:
    def __init__(self, config: Config, bag: Bag):
        self.bag: Bag = bag
        self.population_size: int = config.population_size
        self.current_generation = Generation.create_first_generation(self.bag, self.population_size)
        self.selector: Selector = get_selector(config.selector)
        self.cross_method: Crossover = get_crossover(config.crossover)
        self.mutation_prob: float = config.mutation_prob

    def bag_packer(self):  # todo ver que retornar
        while not self.stop_condition_met(self.current_generation, self.bag):
            self.current_generation.gen_count += 1
            best_fit: float = self.bag.best_fitness(self.current_generation.population)
            if round(self.current_generation.best_fitness) == round(best_fit):
                self.current_generation.cont_same_fitness += 1
            else:
                self.current_generation.cont_same_fitness = 0
                self.current_generation.best_fitness = best_fit
            children = []
            while len(children) < self.population_size:
                parents = np.random.choice(len(self.current_generation.population), 2,
                                           replace=False)  # TODO check si es asi o con selector

                first_parent = self.current_generation.population[parents[0]]
                second_parent = self.current_generation.population[parents[1]]
                [first_child, second_child] = self.cross_method(first_parent, second_parent)
                first_child = mutate(first_child, self.mutation_prob)
                second_child = mutate(second_child, self.mutation_prob)
                children.append(first_child)
                children.append(second_child)
            self.current_generation.population.clear()
            self.current_generation.population.extend(children)

            aux = self.selector(self.current_generation, self.bag, self.population_size)
            self.current_generation.population = aux[:]

        print(f'generation count: {self.current_generation.gen_count}\n')
        print(f'size pop: {len(self.current_generation.population)}')
        for i in range(len(self.current_generation.population)):
            print(f'total weight: {self.bag.calculate_weight(self.current_generation.population[i])}\n'
                  f'total benefit: {self.bag.calculate_benefit(self.current_generation.population[i])}\n')

    def stop_condition_met(self, gen: Generation, bag: Bag) -> bool:
        if gen.gen_count > 500:
            if gen.cont_same_fitness > 5:
                print(f'ENTREEEEEEEEEEEEEE y gane en la generación: {gen.gen_count}')
                return True
            else:
                for i in range(len(gen.population)):
                    if bag.calculate_weight(gen.population[i]) <= bag.max_weight:
                        print('EXITO')
                        print(f'gen: {gen.gen_count}')
                        print(f'total weight: {bag.calculate_weight(gen.population[i])}')
                        return True
        return False
