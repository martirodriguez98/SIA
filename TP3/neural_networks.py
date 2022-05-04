import random
from abc import ABC
import time
from math import tanh

from plot import plot_2d, plot_errors
from config import Param
import numpy as np
from numpy import random, vectorize, tanh, exp, copysign, array


# chequear si la tenemos que definir nosotras o la pasan como parametro
from results import Results

COTA = 10000
n = 0.01
MIN_ERROR = 0.00001


class NeuralNetworkConfig:
    def __init__(self):
        self.x_count: int = 0
        self.normalized = False


class NeuralNetwork(ABC):
    def __init__(self, config_neural: NeuralNetworkConfig):
        self.config_neural: NeuralNetworkConfig = config_neural
        self.plot = {"x": [], "y": [], "errors": []}
        self.time = 0
        self.w = None
        self.x = None
        self.y = None
        self.y_denormalized = None

    def train(self, x: np.ndarray, y: np.ndarray):
        pass

    def get_output(self, input):
        pass

    def predict(self, x):
        print(f'self.x: {self.x}')
        h = x @ self.w
        print(f'w: {self.w}')
        print(f'h: {h}')
        o = []
        for e in h:
            print(h)
            o.append([e])
        #todo normalized case
        return array(o)


class SimpleNeuralNetwork(NeuralNetwork):

    def train(self, x: np.ndarray, y: np.ndarray):
        p: int = len(y)
        i: int = 0
        w = random.uniform(-1, 1, size=self.config_neural.x_count)
        print(f'w: {w}')
        w_min = w
        error: float = 1
        error_min = p * 2
        while (error > 0 and i < COTA):
            i_x = random.randint(0, p)
            print(f'i_x: {i_x}')
            h = np.dot(x[i_x], w)
            o = np.copysign(1, h)
            delta_w = n * (y[i_x] - o) * x[i_x]
            print(f'wa: {w}')
            w = w + delta_w
            print(f'wd: {w}')
            error = self.calculate_error(x, y, w, p)
            # print(error)
            if error < error_min:
                error_min = error
                w_min = w
            print(f'w_min: {w_min}')
            print(f'i:{i}')
            i = i + 1
            print(error_min)
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
        self.x = x
        if self.config_neural.normalized:
            self.y_denormalized = y
            y = 2 * (y - min(y)) / (max(y) - min(y)) - 1
        self.y = y
        p: int = len(y)
        i: int = 0
        w = random.uniform(-1,1, size = self.config_neural.x_count)
        w_min = w
        error: float = 1
        error_min = p * 2

        while error > 0 and i < COTA:
            i_x = random.randint(0, p - 1)
            h = np.dot(x[i_x], w)
            o = self.activation(w, x[i_x])
            delta_w = n * (y[i_x] - o) * x[i_x]
            w = w + delta_w
            error = self.calculate_error(o, y, p)
            self.plot["errors"].append(error)
            if error < error_min:
                print('entreee')
                error_min = error
                w_min = w
            i = i + 1
        self.time = time.time() - self.time
        self.w = w_min
        plot_errors(self.plot, x, y)
        if self.config_neural.normalized:
            return Results(self.y_denormalized, self.predict(self.x), self.time, i, error_min)
        else:
            return Results(self.y, self.predict(self.x), self.time, i, error_min)

    def activation(self, w: np.array, x: np.ndarray):
        o = []
        for i in range(self.config_neural.x_count):
            o.append(w[i] * x[i])
        return sum(o)

    def calculate_error(self, o: float, y: np.ndarray, p: int):
        aux: float = 0
        for i in range(p):
            aux += (y[i] - o) ** 2
        return 0.5 * aux


class NonLinearNeuralNetwork(NeuralNetwork):
    def train(self, x: np.ndarray, y: np.ndarray):
        self.x = x
        if self.config_neural.normalized:
            self.y_denormalized = y
            y = 2 * (y - min(y)) / (max(y) - min(y)) - 1
        self.y = y
        b: float = 0.001
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
            error = self.calculate_error(tanh(b, h), y, p)
            self.plot["errors"].append(error)
            if error < error_min:
                error_min = error
                w_min = w
            i = i + 1
        self.time = time.time() - self.time
        self.w = w_min
        plot_errors(self.plot, self.x, self.y)
        if self.config_neural.normalized:
            return Results(self.y, self.predict(self.x),self.time,i,error_min)
        else:
            return Results(self.y, self.predict(self.x),self.time,i, error_min)

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
        return n * ((y[i_x] - tanh(b, h)) * tanh_der(b, h) * x[i_x])

def tanh_der(b: float, x: float) -> float:
    return b * (1 - tanh(b,x) ** 2)

def tanh(b:float, x: float) -> float:
    return np.tanh(b * x)


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
        self.g = tanh
        self.g_derivative = tanh_der
        self.x = None
        self.y = None
        self.plot2 = dict(
            e=[]
        )
        self.b = 0.4
        self.min_iter = 100000
        self.min_error = 0.005
        self.learning_rate = 0.1
        self.time = 0

        super().__init__(config_neural)


    def train(self, x, y):
        self.x = x
        self.y = y
        self.hidden_layers = [36]
        self.neurons_per_layer = [len(x[0]), *self.hidden_layers, len(y[0])]
        self.layers_count = len(self.neurons_per_layer)
        self.layers = []
        self.time = time.time()

        for i in range(self.layers_count):
            layer = []
            for n in range(self.neurons_per_layer[i]):
                perceptron = Perceptron(None, None, None, None)
                if i != 0 and (n != self.neurons_per_layer[i] - 1 or i == self.layers_count - 1):
                    perceptron.w = random.uniform(-1, 1, size=self.neurons_per_layer[i - 1])
                    perceptron.v = 0
                    perceptron.d = 0
                    perceptron.h = 0
                layer.append(perceptron)
            self.layers.append(layer)

        i = 0
        error = 1
        error_min = len(self.x) * 2
        while error > self.min_error and i < self.min_iter:
            i_x = random.randint(0, len(self.x))

            self.apply_first_layer(i_x)
            self.propagate()
            self.calculate_d_M(self.y[i_x])
            self.retro_propagate()

            error = self.calculate_error(self.x, self.y)[0]
            self.plot2['e'].append(error)
            print(error)
            if error < error_min:
                error_min = error

            self.update_weights()

            i = i + 1
        self.time = time.time() - self.time

        o = []
        for value in self.x:
            o.append(self.predict(value))
        self.plot2['e'].append(error)
        return Results(self.y, array(o), self.time, i, error_min)

    def apply_first_layer(self, i_x):
        for i in range(self.neurons_per_layer[0]):
            self.layers[0][i].v = self.x[i_x][i]

    def propagate(self):
        # Para cada capa oculta hasta la de salida
        for m in range(1, self.layers_count):
            # Para cada neurona i del nivel m
            for i in range(self.neurons_per_layer[m]):
                self.layers[m][i].h = 0
                # Si no es el umbral o la ultima capa
                if i != self.neurons_per_layer[m] - 1 or m == self.layers_count - 1:
                    # Para cada neurona de la capa de abajo sumo el peso
                    for j in range(self.neurons_per_layer[m - 1]):
                        self.layers[m][i].h += self.layers[m][i].w[j] * self.layers[m - 1][j].v
                    self.layers[m][i].v = self.g(self.b, self.layers[m][i].h)
                # Si es el umbral
                else:
                    self.layers[m][i].v = 1

    def calculate_d_M(self, y):
        for i in range(self.neurons_per_layer[-1]):
            perceptron = self.layers[-1][i]
            perceptron.d = self.g_derivative(self.b, perceptron.h) * (y[i] - perceptron.v)

    def retro_propagate(self):
        # Por cada capa oculta de arriba para abajo
        for m in range(self.layers_count - 1, 1, -1):
            # Por cada neurona de la capa m-1
            for i in range(self.neurons_per_layer[m - 1] - 1):
                aux = 0
                # Por cada peso que sale de la neurona m-1
                for j in range(self.neurons_per_layer[m]):
                    if j != self.neurons_per_layer[m] - 1 or m == self.layers_count - 1:
                        aux += self.layers[m][j].w[i] * self.layers[m][j].d

                self.layers[m - 1][i].d = self.g_derivative(self.b, self.layers[m - 1][i].h) * aux

    def update_weights(self):
        # para cada capa de abajo hacia arriba
        for m in range(1, self.layers_count):
            # para cada neurona i del nivel m
            for i in range(self.neurons_per_layer[m]):
                # Para cada neurona de la capa m-1
                if i != self.neurons_per_layer[m] - 1 or m == self.layers_count - 1:
                    for j in range(self.neurons_per_layer[m - 1]):
                        self.layers[m][i].w[j] += self.learning_rate * self.layers[m][i].d * self.layers[m - 1][j].v

    def calculate_error(self, x, y):
        o = []
        for value in x:
            o.append(self.predict(value))
        o = array(o)
        return 0.5 * sum((y - o) ** 2)

    def predict(self, x):
        layers = []

        for i in range(self.layers_count):
            layer = []
            for n in range(self.neurons_per_layer[i]):
                perceptron = Perceptron(None, None, None, None)
                if i != 0 and (n != self.neurons_per_layer[i] - 1 or i == self.layers_count - 1):
                    perceptron.v = 0
                    perceptron.d = 0
                    perceptron.h = 0
                layer.append(perceptron)
            layers.append(layer)

        for i in range(self.neurons_per_layer[0]):
            layers[0][i].v = x[i]

        for m in range(1, self.layers_count):
            for i in range(self.neurons_per_layer[m]):
                if i != self.neurons_per_layer[m] - 1 or m == self.layers_count - 1:
                    for j in range(self.neurons_per_layer[m - 1]):
                        layers[m][i].h += self.layers[m][i].w[j] * layers[m - 1][j].v
                    layers[m][i].v = self.g(self.b, layers[m][i].h)
                else:
                    layers[m][i].v = 1

        return list(map(lambda p: p.v, layers[-1]))


