import sys
import time

from schema import Schema

from bag import Bag, Population
from config_loader import Param, Config
from generation import Generation


class StopCondition:
    def __init__(self):
        self.time = 5 * 60
        self.gen_count = 500
        self.percentage = 50
        self.gen_count_percentage = 20
        self.fitness_gen_count = 20
        self.start_time = 0
        self.unchanged_gens = 0
        self.repeated_individuals: Population = []

    def __repr__(self):
        return f'time: {self.time}\ngen_count: {self.gen_count}\npercentage: {self.percentage}\n' \
               f'gen_count_percentage: {self.gen_count_percentage}\nfitness_gen_count: {self.fitness_gen_count}'

def get_stop_condition(params: Param) -> StopCondition:
    stop_condition: StopCondition = StopCondition()
    if params == None:
        return stop_condition

    try:
        stop_condition.time = params['time']
    except:
        pass
    if stop_condition.time != -1:
        if isinstance(stop_condition.time,int) == False or stop_condition.time < 120:
            raise ValueError(f'Invalid end condition. Time must be a positive integer greater than 120')

    try:
        stop_condition.gen_count = params['gen_count']
    except:
        pass
    if not isinstance(stop_condition.gen_count,int) or stop_condition.gen_count < 500:
        raise ValueError(f'Invalid end condition. Generation count must be an integer over 500')

    try:
        stop_condition.percentage = params['percentage']
    except:
        pass
    if not isinstance(stop_condition.percentage,(float,int)) or stop_condition.percentage < 0 or stop_condition.percentage > 100:
        raise ValueError(f'Invalid end condition. Percentage parameter must be a number between 0 and 100')

    try:
        stop_condition.gen_count_percentage = params['gen_count_percentage']
    except:
        pass
    if not isinstance(stop_condition.gen_count_percentage,int) or stop_condition.gen_count_percentage < 4:
        raise ValueError(f'Invalid end condition. gen_count_percentage must be an integer greater than 4')

    try:
        stop_condition.fitness_gen_count = params['fitness_gen_count']
    except:
        pass
    if not isinstance(stop_condition.fitness_gen_count,int) or stop_condition.fitness_gen_count < 0:
        raise ValueError(f'Invalid end condition. fitness_gen_count must be a positive integer.')
    return stop_condition

def stop_condition_met(stop_condition: StopCondition, gen: Generation, bag: Bag) -> bool:
    if gen.gen_count > stop_condition.gen_count:
        if time.perf_counter() > stop_condition.time:
            if valid_solution(gen,bag):
                print('Time is over. A solution was found.')
            else:
                print('Time is over. A solution could not be found.')
            return True

        if unchanged_generations(stop_condition,gen,bag):
            print(f'{stop_condition.percentage}% of the population has remain the same for over {stop_condition.unchanged_gens} generations.')
            return True

        if fitness_gen_count(stop_condition,gen,bag):
            print(f'The best fitness has been the same over {stop_condition.fitness_gen_count} generations')
            return True

    return False

def valid_solution(gen: Generation, bag: Bag) -> bool:
    best_ind,best_fit,weight = bag.best_individual(gen.population)
    if weight <= bag.max_weight:
        return True
    return False

def fitness_gen_count(stop_condition: StopCondition, gen: Generation, bag: Bag) -> bool:
    if gen.cont_same_fitness >= stop_condition.fitness_gen_count:
        return valid_solution(gen,bag)
    return False

def unchanged_generations(stop_condition: StopCondition,gen: Generation,bag: Bag):
    if stop_condition.unchanged_gens >= stop_condition.gen_count_percentage:
        return valid_solution(gen,bag)
    return False

def update_changed_population(stop_condition: StopCondition, generation: Generation, bag: Bag):
    new_repeated = []
    for ind in generation.population:
        if ind in stop_condition.repeated_individuals:
            new_repeated.append(ind)

    if (len(new_repeated) / len(generation.population)) * 100 >= stop_condition.percentage:
        stop_condition.unchanged_gens += 1
    else:
        stop_condition.unchanged_gens = 0

    stop_condition.repeated_individuals.clear()

    if len(new_repeated) != 0:
        for i in new_repeated:
            stop_condition.repeated_individuals.append(i)
    else:
        stop_condition.repeated_individuals.extend(generation.population)
