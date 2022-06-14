import time
from random import random

import numpy as np
from numpy import array
from results import Results


class Perceptron:
    def __init__(self, w, v, d, h):
        self.w = w
        self.v = v
        self.d = d
        self.h = h

    def __repr__(self):
        return f'w: {self.w}\tv: {self.v}\td: {self.d}\th: {self.h}\n'

def tanh_der(b: float, x: float) -> float:
    return b * (1 - tanh(b, x) ** 2)


def tanh(b: float, x: float):
    return np.tanh(b * x)

class MultilayerNeuralNetwork():
    def __init__(self, layers):
        self.perceptrons = None
        self.layers = layers
        self.len_layers = 0
        self.g = tanh
        self.g_derivative = tanh_der
        self.x = None
        self.y = None
        self.plot2 = dict(
            e=[]
        )
        self.b = 0.5
        self.min_iter = 10000
        self.min_error = 0.001
        self.learning_rate = 0.01
        self.time = 0


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
