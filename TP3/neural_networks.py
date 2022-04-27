import random
from abc import ABC
from math import tanh

from plot import plot_2d, plot_errors
from config import Param
import numpy as np
from typing import Callable

# chequear si la tenemos que definir nosotras o la pasan como parametro
COTA = 500
n = 0.1
MIN_ERROR = 0.05


class NeuralNetworkConfig:
    def __init__(self):
        self.x_count: int = 0


class NeuralNetwork(ABC):
    def __init__(self, config_neural: NeuralNetworkConfig):
        self.config_neural: NeuralNetworkConfig = config_neural
        self.plot = {"x": [], "y": [], "errors": []}

    def train(self, x: np.ndarray, y: np.ndarray):
        pass

    def get_output(self, input):
        pass


class SimpleNeuralNetwork(NeuralNetwork):

    def train(self, x: np.ndarray, y: np.ndarray):
        p: int = len(y)
        i: int = 0
        w = np.zeros(self.config_neural.x_count)
        w_min = w
        error: float = 1
        error_min = p * 2
        while error > 0 and i < COTA:
            i_x = random.randint(0, p - 1)
            h = np.dot(x[i_x], w)
            o = np.copysign(1, h)
            delta_w = n * (y[i_x] - o) * x[i_x]
            w = w + delta_w
            error = self.calculate_error(x, y, w, p)
            # print(error)
            if error < error_min:
                error_min = error
                w_min = w
            i = i + 1
        self.plot["x"].append(np.arange(-2, 4))
        self.plot["y"].append((-w_min[1] / w_min[2]) * np.arange(-2, 4) - w_min[0] / w_min[2])
        plot_2d(self.plot, x, y)

    def calculate_error(self, x: np.ndarray, y: np.ndarray, w: np.array, p: int):
        o = []
        for i in range(p):
            o.append(abs(y[i] - np.copysign(1, np.dot(x[i], w))))
        return sum(o)


class LinearNeuralNetwork(NeuralNetwork):

    def train(self, x: np.ndarray, y: np.ndarray):
        p: int = len(y)
        i: int = 0
        w = np.zeros(self.config_neural.x_count)
        w_min = w
        error: float = 1
        error_min = p * 2

        while error > 0 and i < COTA:
            i_x = random.randint(0, p - 1)
            h = np.dot(x[i_x], w)
            o = self.activation(w, x)
            delta_w = n * (y[i_x] - o) * x[i_x]
            w = w + delta_w
            error = self.calculate_error(o, y, p)
            self.plot["errors"].append(error)
            if error < error_min:
                error_min = error
                w_min = w
            i = i + 1
        plot_errors(self.plot, x, y)

    def activation(self, w: np.array, x: np.ndarray):
        o: float = 0
        for i in range(self.config_neural.x_count):
            o += sum(w[i] * x[i])
        return o

    def calculate_error(self, o: float, y: np.ndarray, p: int):
        aux: float = 0
        for i in range(p):
            aux += (y[i] - o) ** 2
        return 0.5 * aux


class NonLinearNeuralNetwork(NeuralNetwork):
    def train(self, x: np.ndarray, y: np.ndarray):
        b: float = 0.005
        p: int = len(y)
        i: int = 0
        w = np.zeros(self.config_neural.x_count)
        w_min = w
        error: float = 1
        error_min = p * 2

        while error > 0 and i < COTA:
            i_x = random.randint(0, p - 1)
            h = self.excitation(w, x)
            delta_w = self.calculate_delta_w(x, y, p, i_x, h, b)
            w = w + delta_w
            error = self.calculate_error(tanh(h * b), y, p)
            self.plot["errors"].append(error)
            if error < error_min:
                error_min = error
                w_min = w
            i = i + 1
        plot_errors(self.plot, x, y)

    def excitation(self, w: np.array, x: np.ndarray):
        o: float = 0
        for i in range(self.config_neural.x_count):
            o += sum(w[i] * x[i])
        return o

    def calculate_error(self, o: float, y: np.ndarray, p: int):
        aux: float = 0
        for i in range(p):
            aux += (y[i] - o) ** 2
        return 0.5 * aux

    def calculate_delta_w(self, x: np.ndarray, y: np.ndarray, p: int, i_x: int, h: float, b: float):
        return n * ((y[i_x] - tanh(h * b)) * tanh_der(h, b) * x[i_x])

def tanh_der(x: float, b: float) -> float:
    return b * (1 - tanh(x * b) ** 2)


class Perceptron:
    def __init__(self, w, v, d, h):
        self.w = w
        self.v = v
        self.d = d
        self.h = h

    def __repr__(self):
        return f'w: {self.w}\tv: {self.v}\td: {self.d}\th: {self.h}\n'

class MultilayerNeuralNetwork(NeuralNetwork):
    def __init__(self, config_neural: NeuralNetworkConfig):
        self.perceptrons = None
        self.layers = None
        self.len_layers = 0
        self.b = 0.05

    def train(self, x: np.ndarray, y: np.ndarray):
        b: float = 0.05
        p: int = len(y)
        #todo acordarse que la primera capa tiene que ser del tamaño de la entrada
        self.layers: list = [len(x[0]), 4, len(y)]
        error = 1
        self.len_layers = len(self.layers)
        self.perceptrons = [None] * self.len_layers

        for i in range(self.len_layers):
            self.perceptrons[i] = [None] * self.layers[i]
            for j in range(self.layers[i]):
                self.perceptrons[i][j] = Perceptron(None, None, None, None)
                if i != self.len_layers-1: #si no es la ultima capa
                    self.perceptrons[i][j].w = [0] * self.layers[i+1]
                    for w in range(self.layers[i+1]):
                        self.perceptrons[i][j].w[w] = random.random()

        while error > MIN_ERROR:
            i_x = random.randint(0, p - 1)
            # 2. aplicamos entrada a capa 0
            for j in range(self.layers[0]):
                self.perceptrons[0][j].v = x[i_x][j]

            # 3. propagamos entrada hasta a capa de salida
            self.propagate()
            # for i in range(len_layers):
            #     if i == 0:
            #         i=1
            #     for j in range(self.layers[i]):
            #         for k in range(self.layers[i-1]):
            #             self.perceptrons[i][j].v, self.perceptrons[i][j].h = self.calculate_v(self.perceptrons[i-1], j, b)

            # 4. calcular d para la capa de salida
            last_index = self.len_layers-1
            for i in range(self.layers[last_index]):
                aux = tanh_der(self.perceptrons[last_index][i].h, b) * (y[i] - self.perceptrons[last_index][i].v)[0]
                self.perceptrons[last_index][i].d = aux

            # 5. Retropropagamos d
            for j in range(self.len_layers-1-1): #es entre M y 2
                index = self.len_layers - 1 - j - 1 #la ultima capa no la cuento
                for i in range(self.layers[index]):
                    self.perceptrons[index][i].d = self.calculate_delta(self.perceptrons[index][i].h, self.perceptrons[index][i].w, self.perceptrons[index+1], b)

            # 6. Actualizamos pesos
            for i in range(self.len_layers-1):
                for j in range(self.layers[i]):
                    for k in range(self.layers[i+1]):
                        delta_w = n * self.perceptrons[i+1][k].d * self.perceptrons[i][j].v
                        self.perceptrons[i][j].w[k] += delta_w

            # 7. calcular error
            error = self.calculate_error(self.perceptrons, y, b)
        print(self.perceptrons)


    def propagate(self):
        for i in range(self.len_layers):
            if i == 0:
                i=1
            for j in range(self.layers[i]):
                for k in range(self.layers[i-1]):
                    self.perceptrons[i][j].v, self.perceptrons[i][j].h = self.calculate_v(self.perceptrons[i-1], j, self.b)

    def calculate_error(self, perceptrons, y, b):
        sum = 0
        last_layer = len(self.layers)-1
        for i in range(self.layers[last_layer]):
            o = tanh(perceptrons[last_layer][i].h * b)
            sum += (y[i] - o) ** 2
        return 0.5 * sum

    def calculate_delta(self, h, w, layer, b):
        sum = 0
        for i in range(len(layer)):
            sum += w[i] * layer[i].d
        return tanh_der(h, b) * sum

    def calculate_v(self, layer, index, b):
        h = 0
        for i in range(len(layer)):
            h += layer[i].v * layer[i].w[index]
        return tanh(h * b), h

    def create_v0(self, x_i_x):
        v0 = [0] * len(x_i_x)
        for i in range(len(x_i_x)):
            v0[i] = x_i_x[i]
        return v0

    def calculate_h(self, w, v):
        h: float = 0
        print(f'v: {v}')
        for j in range(len(v)):
            h += v[j].v * w[j]
        return h

    def get_output(self, input):
        print('en get output')
        aux_input: np.ndarray = np.ones((len(input), len(input[0]) + 1))
        for i in range(len(input)):
            for j in range(len(input[i])):
                aux_input[i][j + 1] = input[i][j]
        x = aux_input
        output = []
        for i in range(len(aux_input)):
            for j in range(self.layers[0]):
                self.perceptrons[0][j].v = aux_input[i][j]
            self.propagate()
            print(self.perceptrons[self.len_layers-1])
            output.append([self.perceptrons[self.len_layers-1][i].v])
        return output

