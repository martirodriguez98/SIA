import random

from numpy import average

from bag import Bag
from config_loader import Config
from generation import Generation
from mutation import mutate
from parent_crossing import get_crossover, Crossover
from selection import Selector, get_selector
from stop_condition import StopCondition, get_stop_condition, stop_condition_met, update_changed_population


class Resolver:
    def __init__(self, config: Config, bag: Bag):
        self.bag: Bag = bag
        self.population_size: int = config.population_size
        self.current_generation = Generation.create_first_generation(self.bag, self.population_size)
        self.selector: Selector = get_selector(config.selector)
        self.cross_method: Crossover = get_crossover(config.crossover)
        self.mutation_prob: float = config.mutation_prob
        self.stop_condition: StopCondition = get_stop_condition(config.stop_condition)
        self.plot = {"min_fitness": [], "max_fitness": [], "avg_fitness": []}

    def bag_packer(self):
        self.stop_condition.repeated_individuals = self.current_generation.population.copy()

        while not stop_condition_met(self.stop_condition,self.current_generation, self.bag):
            self.current_generation.gen_count += 1
            best_fit: float = self.bag.best_fitness(self.current_generation.population)
            if self.current_generation.best_fitness == best_fit:
                self.current_generation.cont_same_fitness += 1
            else:
                self.current_generation.cont_same_fitness = 0
                self.current_generation.best_fitness = best_fit
            new_gen = set()
            for i in self.current_generation.population:  # agrego los padres a la nueva generacion
                new_gen.add(tuple(i))
            while len(new_gen) < 2 * self.population_size:
                parents = random.sample(self.current_generation.population, 2)
                first_parent = parents[0]
                second_parent = parents[1]
                [first_child, second_child] = self.cross_method(first_parent, second_parent)
                first_child = mutate(first_child, self.mutation_prob)
                second_child = mutate(second_child, self.mutation_prob)
                if tuple(first_child) not in new_gen:
                    new_gen.add(tuple(first_child))
                if len(new_gen) < 2 * self.population_size:
                    if tuple(second_child) not in new_gen:
                        new_gen.add(tuple(second_child))
            cur_gen_list = []
            for i in new_gen:
                cur_gen_list.append(list(i))
            min_fitness: float = 10000000000
            for i in self.current_generation.population:
                aux = self.bag.calculate_total_fitness(i)
                if aux < min_fitness:
                    min_fitness = aux

            self.plot["avg_fitness"].append(
                average([self.bag.calculate_total_fitness(i) for i in self.current_generation.population]))
            self.plot["min_fitness"].append(min_fitness)
            self.plot["max_fitness"].append(best_fit)

            gen_aux = Generation(cur_gen_list, self.current_generation.gen_count)
            aux = self.selector(gen_aux, self.bag, self.population_size)
            self.current_generation.population.clear()
            for i in aux:
                self.current_generation.population.append(i)

            update_changed_population(self.stop_condition, self.current_generation, self.bag)

        print(f'generation count: {self.current_generation.gen_count}\n')
        for i in range(len(self.current_generation.population)):
            print(f'total weight: {self.bag.calculate_weight(self.current_generation.population[i])}\n'
                  f'total benefit: {self.bag.calculate_benefit(self.current_generation.population[i])}\n'
                  f'fitness: {self.bag.calculate_total_fitness(self.current_generation.population[i])}')

    def get_plot(self):
        return self.plot


