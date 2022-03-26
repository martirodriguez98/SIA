import numpy as np

from bag import Individual


def mutate(individual: Individual, mutation_prob: float) -> Individual:
    new_individual: Individual = []
    for i in range(len(individual)):
        r = np.random.random()
        if r < mutation_prob:
            new_individual.insert(i, 1 - individual[i])
        else:
            new_individual.insert(i, individual[i])
    return new_individual
