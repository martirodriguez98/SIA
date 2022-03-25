from typing import Set, Tuple, List

import numpy as np

import bag
from bag import Bag
from config_loader import Config
from data_loader import Item
from generation import Generation, Population
from mutation import mutate
from parent_crossing import cross_individuals
from selection import Selector, get_selector


class Resolver:
    def __init__(self, config: Config, bag: Bag):
        self.bag: Bag = bag
        self.population_size: int = config.population_size
        self.current_generation = Generation.create_first_generation(self.bag, self.population_size)
        self.selector: Selector = get_selector(config.selector)
        self.cross_method: Crossover = get_crossover(config.cross_method)
        self.mutation_prob: Mutator =get_mutator(config.mutation_prob)


    def bag_packer(self): #todo ver que retornar
        while not self.stop_condition_met():
            self.current_generation.gen_count += 1

            children = []
            while len(children) < self.population_size:
                [first_parent, second_parent] = np.random.choice(self.current_generation.population,2, replace=False) #TODO check si es asi o con selector
                [first_child, second_child] = cross_individuals(first_parent,second_parent,self.cross_method)
                first_child = mutate(first_child,self.mutation_prob)
                second_child = mutate(second_child,self.mutation_prob)
                children.append(first_child)
                children.append(second_child)

            children.extend(self.current_generation.population)
            children = self.selector(children,self.population_size)

            for idx, individual in enumerate(children):
                self.current_generation[idx] = individual


    def stop_condition_met(self) -> bool:
        return False