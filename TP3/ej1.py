import sys

import numpy as np

from config import Config, Param
from config_loader import get_set, get_neural_network
from neural_networks import NeuralNetwork


def ej1(config_file: str):
    config: Config = Config(config_file)
    training_set: Param = config.training_set

    #TODO agregar en el readme que el default es el set de and
    if not training_set or training_set['x'] is None:
        training_set['x'] = 'training_sets/x/ej1_and.tsv'
    if not training_set or training_set['y'] is None:
        training_set['y'] = 'training_sets/y/ej1_and.tsv'

    x: np.ndarray = get_set(training_set['x'], training_set['x_line_count'])
    y: np.ndarray = get_set(training_set['y'], training_set['y_line_count'])

    neural_network: NeuralNetwork = get_neural_network(config.network, len(x[0]))()


if __name__ == '__main__':
    argv = sys.argv

    config_file: str = 'config.yaml'
    if len(argv) > 1:
        config_file = argv[1]

    try:
        ej1(config_file)

    except ValueError as e:
        print(f'Error found in {config_file}\n{e}')

    except FileNotFoundError as e:
        print(f'Configuration file {e.filename} not found')

    except KeyboardInterrupt:
        print('Program was interrupted. Optimization ended incomplete.')
