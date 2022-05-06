import math
import sys
import random
from itertools import chain

import numpy as np

from config import Config, Param
from config_loader import get_set, get_neural_network
from neural_networks import NeuralNetwork
from plot import plot_2d, plot_prediction


def ej2(config_file: str):
    config: Config = Config(config_file)
    training_set: Param = config.training_set

    # TODO agregar en el readme que el default es el set de and
    if not training_set or training_set['x'] is None:
        training_set['x'] = 'training_sets/x/ej2_in.tsv'
    if not training_set or training_set['y'] is None:
        training_set['y'] = 'training_sets/y/ej2_out.tsv'

    x: np.ndarray = get_set(training_set['x'], training_set['x_line_count'], False)
    # agregamos un espacio para el umbral seteado en 1
    new_x: np.ndarray = np.ones((len(x), len(x[0]) + 1))
    for i in range(len(x)):
        for j in range(len(x[i])):
            new_x[i][j + 1] = x[i][j]
    x = new_x

    y: np.ndarray = get_set(training_set['y'], training_set['y_line_count'], config.network['normalize'])
    
    neural_network: NeuralNetwork = get_neural_network(config.network, len(x[0]))()
    results = neural_network.train(x, y)
    results.print()
    #plot prediction
    plot_prediction(results)


def ej2b(config_file: str):
    config: Config = Config(config_file)
    training_set: Param = config.training_set

    # TODO agregar en el readme que el default es el set de and
    if not training_set or training_set['x'] is None:
        training_set['x'] = 'training_sets/x/ej2_in.tsv'
    if not training_set or training_set['y'] is None:
        training_set['y'] = 'training_sets/y/ej2_out.tsv'

    x: np.ndarray = get_set(training_set['x'], training_set['x_line_count'], False)
    # agregamos un espacio para el umbral seteado en 1
    new_x: np.ndarray = np.ones((len(x), len(x[0]) + 1))
    for i in range(len(x)):
        for j in range(len(x[i])):
            new_x[i][j + 1] = x[i][j]
    x = new_x

    y: np.ndarray = get_set(training_set['y'], training_set['y_line_count'], config.network['normalize'])

    #dividir x en k e ir agarrando un k de testeo y los k-1 restantes de entrenamiento
    k = 10
    items_per_k = math.ceil(len(x) / k)

    k_x = []
    k_y = []
    for i in range(0, k):
        aux_x = []
        aux_y = []
        for j in range(0,items_per_k):
            r = random.randint(0, len(x) - 1)
            aux_x.append(x[r])
            aux_y.append(y[r])
            x = np.delete(x, r, axis=0)
            y = np.delete(y, r, axis=0)
        k_x.append(aux_x)
        k_y.append(aux_y)

    r_aux = np.arange(0, k)
    random.shuffle(r_aux)
    for i in range(0, k):
        testing = k_x[r_aux[i]]
        testing_y = k_y[r_aux[i]]
        training = []
        training_y = []
        for j in range(len(k_x)):
            if j != r_aux[i]:
                training.append(k_x[j])
                training_y.append(k_y[j])
        training = list(chain(*training))
        training_y = list(chain(*training_y))
        neural_network: NeuralNetwork = get_neural_network(config.network, len(k_x[0][0]))()
        results = neural_network.train(training, training_y)
        predicted = neural_network.predict(testing)
        plot_prediction(predicted, testing_y, f"Prediction for {i}","Element set","Prediction")
        neural_network.reset_network()
    # results.print()
    # # plot prediction
    # plot_prediction(results)

if __name__ == '__main__':
    argv = sys.argv

    config_file: str = 'config.yaml'
    if len(argv) > 1:
        config_file = argv[1]

    try:
        ej2b(config_file)

    except ValueError as e:
        print(f'Error found in {config_file}\n{e}')

    except FileNotFoundError as e:
        print(f'Configuration file {e.filename} not found')

    except KeyboardInterrupt:
        print('Program was interrupted. Optimization ended incomplete.')
