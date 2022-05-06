import math
import random
import sys
from itertools import chain

import numpy as np

from config import Config, Param
from config_loader import get_set, get_neural_network
from neural_networks import NeuralNetwork
from plot import plot_prediction


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

    x: np.ndarray = get_set(training_set['x'], training_set['x_line_count'], False)
    new_x: np.ndarray = np.ones((len(x), len(x[0]) + 1))
    for i in range(len(x)):
        for j in range(len(x[i])):
            new_x[i][j + 1] = x[i][j]
    x = new_x

    y: np.ndarray = get_set(training_set['y'], training_set['y_line_count'], False)

    k = 5
    items_per_k = math.ceil(len(x) / k)
    k_x = []
    k_y = []
    for i in range(0,k):
        aux_x = []
        aux_y = []
        for j in range(0, items_per_k):
            r = random.randint(0, len(x) - 1)
            aux_x.append(x[r])
            aux_y.append(y[r])
            x = np.delete(x, r, axis=0)
            y = np.delete(y, r, axis=0)
        k_x.append(aux_x)
        k_y.append(aux_y)

    r_aux = np.arange(0,k)
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
        #testeamos
        predictions = []
        for m in range(len(testing)):
            predictions.append(neural_network.predict(testing[m]))
        plot_prediction(predictions, testing_y, f"Predictions for testing in iteration {i}", "Bit","Prediction")
        neural_network.reset_network()



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

    # neural_network: NeuralNetwork = get_neural_network(config.network, len(x[0]))()
    # results = neural_network.train(training_set, training_expected)
    # results.print()


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
    for k in range(len(testing_set)):
        predicted = neural_network.predict(testing_set[k])
        print(predicted)
        plot_prediction(predicted, testing_expected[k],f"Prediction for {k}","Bit","Prediction")

if __name__ == '__main__':
    argv = sys.argv

    config_file: str = 'config.yaml'
    if len(argv) > 1:
        config_file = argv[1]

    try:
        # ej3(config_file)
        # ej3c(config_file)
        ej3b(config_file)
    except ValueError as e:
        print(f'Error found in {config_file}\n{e}')

    except FileNotFoundError as e:
        print(f'Configuration file {e.filename} not found')

    except KeyboardInterrupt:
        print('Program was interrupted. Optimization ended incomplete.')
