import math
import random
import sys

import numpy as np

from config import Config, Param
from config_loader import get_set, get_neural_network
from neural_networks import NeuralNetwork


def ej3(config_file: str):
    config: Config = Config(config_file)
    training_set: Param = config.training_set

    # TODO agregar en el readme que el default es el set de and
    if not training_set or training_set['x'] is None:
        training_set['x'] = 'training_sets/x/ej1_xor.tsv'
    if not training_set or training_set['y'] is None:
        training_set['y'] = 'training_sets/y/ej1_xor.tsv'

    x: np.ndarray = get_set(training_set['x'], training_set['x_line_count'], False)
    # agregamos un espacio para el umbral seteado en 1
    new_x: np.ndarray = np.ones((len(x), len(x[0]) + 1))
    for i in range(len(x)):
        for j in range(len(x[i])):
            new_x[i][j + 1] = x[i][j]
    x = new_x

    y: np.ndarray = get_set(training_set['y'], training_set['y_line_count'], False)

    neural_network: NeuralNetwork = get_neural_network(config.network, len(x[0]))()
    results = neural_network.train(x, y)
    results.print()

def ej3b(config_file: str):
    config: Config = Config(config_file)
    training_set: Param = config.training_set
    if not training_set or training_set['x'] is None:
        training_set['x'] = 'training_sets/x/ej3.tsv'
    if not training_set or training_set['y'] is None:
        training_set['y'] = 'training_sets/y/ej3.tsv'

    training_size = 0.8 #todo parametrizar, numero entre 0 y 1 (mayor a 0)

    x: np.ndarray = get_set(training_set['x'], training_set['x_line_count'], False)
    new_x: np.ndarray = np.ones((len(x), len(x[0]) + 1))
    for i in range(len(x)):
        for j in range(len(x[i])):
            new_x[i][j + 1] = x[i][j]
    x = new_x

    y: np.ndarray = get_set(training_set['y'], training_set['y_line_count'], False)

    total_inputs = len(x)
    limit = math.ceil(total_inputs * training_size)

    training_set = []
    testing_set = []
    training_expected = []
    testing_expected = []

    # entrenamos #training_size pero los elegimos de manera random
    for i in range(limit):
        r = random.randint(0, len(x)-1)
        training_set.append(x[r])
        training_expected.append(y[r])
        x = np.delete(x, r, axis=0)
        y = np.delete(y, r, axis=0)

    for i in range(len(x)):
        testing_set.append(x[i])
        testing_expected.append(y[i])

    #los entrenamos en orden y despues no importa lo que testeamos, devuelve par, impar, par, etc
    # training_set = x[:limit]
    # testing_set = x[limit:]

    # training_expected = y[:limit]
    # testing_expected = y[limit:]

    #entrenamos todos los pares y testeamos los impares
    # training_set = []
    # testing_set = []
    # training_expected = []
    # testing_expected = []
    #
    # for i in range(len(x)):
    #     if i % 2 == 0:
    #         training_set.append(x[i])
    #         training_expected.append(y[i])
    #     else:
    #         testing_set.append(x[i])
    #         testing_expected.append(y[i])

    neural_network: NeuralNetwork = get_neural_network(config.network, len(x[0]))()
    results = neural_network.train(training_set, training_expected)
    results.print()


def ej3c(config_file: str):
    config: Config = Config(config_file)
    training_set: Param = config.training_set
    if not training_set or training_set['x'] is None:
        training_set['x'] = 'training_sets/x/ej3.tsv'
    if not training_set or training_set['y'] is None:
        training_set['y'] = 'training_sets/y/ej3c.tsv'

    training_size = 0.8 #todo parametrizar, numero entre 0 y 1 (mayor a 0)

    x: np.ndarray = get_set(training_set['x'], training_set['x_line_count'], False)
    new_x: np.ndarray = np.ones((len(x), len(x[0]) + 1))
    for i in range(len(x)):
        for j in range(len(x[i])):
            new_x[i][j + 1] = x[i][j]
    x = new_x

    y: np.ndarray = get_set(training_set['y'], training_set['y_line_count'], False)

    total_inputs = len(x)

    #agregamos con probabilidad 0.02 ruido a los digitos para testear
    testing_set: np.ndarray = np.zeros((len(x), len(x[0])))
    testing_expected: np.ndarray = np.zeros((len(y), len(y[0])))

    for i in range(len(x)):
        for j in range(len(x[i])):
            r = random.random()
            if r <= 0.02:
                testing_set[i][j] = not x[i][j]
            else:
                testing_set[i][j] = x[i][j]

    for i in range(len(y)):
        for j in range(len(y[i])):
            testing_expected[i][j] = (y[i][j])

    neural_network: NeuralNetwork = get_neural_network(config.network, len(x[0]))()
    results = neural_network.train(x, y)
    results.print()

if __name__ == '__main__':
    argv = sys.argv

    config_file: str = 'config.yaml'
    if len(argv) > 1:
        config_file = argv[1]

    try:
        # ej3(config_file)
        # ej3b(config_file)
        ej3c(config_file)
    except ValueError as e:
        print(f'Error found in {config_file}\n{e}')

    except FileNotFoundError as e:
        print(f'Configuration file {e.filename} not found')

    except KeyboardInterrupt:
        print('Program was interrupted. Optimization ended incomplete.')
