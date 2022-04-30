import random
from abc import ABC
from math import tanh

from plot import plot_2d, plot_errors
from config import Param
import numpy as np
from typing import Callable

# chequear si la tenemos que definir nosotras o la pasan como parametro
COTA = 100000
n = 0.1
MIN_ERROR = 0.005


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
        self.b = 0.4
        super().__init__(config_neural)

    def train(self, x: np.ndarray, y: np.ndarray):
        p: int = len(y)
        #todo acordarse que la primera capa tiene que ser del tamaño de la entrada
        self.layers: list = [len(x[0]), 3 , len(y[0])]
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
                        if w == self.layers[i+1]:
                            self.perceptrons[i][j].w[w] = 1
                        self.perceptrons[i][j].w[w] = random.random()

        cota = 0
        while error > MIN_ERROR and cota < COTA:
            i_x = random.randint(0, p - 1)
            # 2. aplicamos entrada a capa 0
            for j in range(self.layers[0]):
                if j == self.layers[0] - 1: #umbral
                    self.perceptrons[0][j].v = 1
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
                if i != self.layers[last_index] - 1: #salteamos umbral
                    aux = tanh_der(self.perceptrons[last_index][i].h, self.b) * (y[i_x][i] - self.perceptrons[last_index][i].v)
                    self.perceptrons[last_index][i].d = aux

            #   -   -   -   -   -
            # 5. Retropropagamos d
            for j in range(self.len_layers-1-1): #es entre M y 2
                index = self.len_layers - 1 - j - 1 #la ultima capa no la cuento
                for i in range(self.layers[index]):
                    if i != self.layers[index] - 1:  # salteamos umbral
                        self.perceptrons[index][i].d = self.calculate_delta(self.perceptrons[index][i].h, self.perceptrons[index][i].w, self.perceptrons[index+1])

            # 6. Actualizamos pesos
            for i in range(self.len_layers):
                for j in range(self.layers[i]):
                    if j != self.layers[i] - 1 and i+1 < len(self.layers) - 1:
                        for k in range(self.layers[i+1]):
                            if k != self.layers[i+1] - 1 and i+1 != self.len_layers - 1:
                                delta_w = n * self.perceptrons[i+1][k].d * self.perceptrons[i][j].v
                                self.perceptrons[i][j].w[k] += delta_w

            # 7. calcular error
            error = self.calculate_error(self.perceptrons, y, x)[0]
            print(error)
            cota += 1
        # print(self.perceptrons)


    def propagate(self):
        for i in range(self.len_layers):
            if i == 0:
                i=1
            for j in range(self.layers[i]):
                for k in range(self.layers[i-1]):
                    self.perceptrons[i][j].v, self.perceptrons[i][j].h = self.calculate_v(self.perceptrons[i-1], j)

    def calculate_error(self, perceptrons, y, x):
        o = []
        last_layer = self.len_layers - 1
        for value in x:
            o.append(self.predict(value))
        o = np.array(o)
        return 0.5 * sum((y - o) ** 2)

    def predict(self, x):
        layers = []
        for i in range(self.len_layers):
            layer = []
            for n in range(self.layers[i]):
                perceptron = Perceptron(None, None, None, None)
                if i != 0 and (n != self.layers[i] - 1 or i == self.len_layers - 1):
                    perceptron.v = 0
                    perceptron.d = 0
                    perceptron.h = 0
                layer.append(perceptron)
            layers.append(layer)

        for i in range(self.layers[0]):
            layers[0][i].v = x[i]

        for m in range(1, self.len_layers-1):
            for i in range(self.layers[m]):
                if i != self.layers[m] - 1:
                    for j in range(self.layers[m + 1]):
                        if j != self.layers[m + 1] - 1:
                            layers[m][i].h += self.perceptrons[m][i].w[j] * layers[m + 1][j].v
                    layers[m][i].v = tanh(self.b * layers[m][i].h)
                else:
                    layers[m][i].v = 1
        print(layers)
        return list(map(lambda p: p.v, layers[-1]))

    def calculate_delta(self, h, w, layer):
        sum = 0
        for i in range(len(layer)):
            if i != len(layer) - 1:
                sum += w[i] * layer[i].d
        return tanh_der(h, self.b) * sum

    def calculate_v(self, layer, index):
        h = 0
        for i in range(len(layer)):
            h += layer[i].v * layer[i].w[index]
        return tanh(h * self.b), h

    def create_v0(self, x_i_x):
        v0 = [0] * len(x_i_x)
        for i in range(len(x_i_x)):
            v0[i] = x_i_x[i]
        return v0

    def calculate_h(self, w, v):
        h: float = 0
        for j in range(len(v)):
            h += v[j].v * w[j]
        return h

    def get_output(self, input):
        aux_input: np.ndarray = np.ones((len(input), len(input[0]) + 1))
        for i in range(len(input)):
            for j in range(len(input[i])):
                aux_input[i][j + 1] = input[i][j]
        x = aux_input
        output: np.ndarray = np.zeros((len(x), self.layers[self.len_layers-1]))
        for i in range(len(x)):
            for j in range(self.layers[0]):
                self.perceptrons[0][j].v = x[i][j]
            self.propagate()
            for k in range(self.layers[self.len_layers-1]):
                output[i][k] = self.perceptrons[self.len_layers - 1][k].v
        return output

