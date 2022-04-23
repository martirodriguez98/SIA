import random
from abc import ABC
from plot import plot_2d, plot_errors
from config import Param
import numpy as np
from typing import Callable

# chequear si la tenemos que definir nosotras o la pasan como parametro
COTA = 100
n = 0.001
MIN_ERROR = 0.01


class NeuralNetworkConfig:
    def __init__(self):
        self.x_count: int = 0


class NeuralNetwork(ABC):
    def __init__(self, config_neural: NeuralNetworkConfig):
        self.config_neural: NeuralNetworkConfig = config_neural
        self.plot = {"x": [], "y": [], "errors": []}

    def train(self, x: np.ndarray, y: np.ndarray):
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
            print(error)
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
        aux = []
        for i in range(p):
            aux.append(0.5 * pow(abs(y[i] - o), 2))
        return sum(aux)


class NonLinearNeuralNetwork(NeuralNetwork):
    def train(self, x: np.ndarray, y: np.ndarray):
        b: float = 0.01
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
            error = self.calculate_error(tanh(h, b), y, p)
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
            aux += 0.5 * pow(abs(y[i] - o), 2)
        return aux

    def calculate_delta_w(self, x: np.ndarray, y: np.ndarray, p: int, i_x: int, h: float, b: float):
        delta_w: float = 0
        for i in range(p):
            delta_w += (y[i_x] - tanh(h, b)) * tanh_der(h, b) * x[i_x]
        return n * delta_w


def tanh(x: float, b: float) -> float:
    return np.tanh(b * x)


def tanh_der(x: float, b: float) -> float:
    return b * (1 - tanh(x, b) ** 2)


class Perceptron:
    def __init__(self, w, v, d, h):
        self.w = w
        self.v = v
        self.d = d
        self.h = h

    def __repr__(self):
        return f'w: {self.w}\tv: {self.v}\td: {self.d}\th: {self.h}\n'

class MultilayerNeuralNetwork(NeuralNetwork):
    def train(self, x: np.ndarray, y: np.ndarray):
        # b: float = 0.05
        # p: int = len(y)
        # layers: list = [3, 2, 4]
        # conjunto de pesos en valores pequeños al azar

        # error: float = 1
        # # TODO parametrizar
        # layers: list = [3, 2, 4]
        # v_layer = [0] * len(layers)
        # d: list = [0] * len(layers)
        # w: list = [0] * len(layers)
        # h: list = [0] * len(layers)
        # for i in range(len(v_layer)):
        #     v_layer[i] = [0] * (layers[i])
        #     w[i] = [0] * (layers[i])
        #     h[i] = [0] * (layers[i])
        #     d[i] = [0] * (layers[i])
        #     for j in range(layers[i]):
        #         w[i][j] = random.random()
        # while error > MIN_ERROR:
        #     i_x = random.randint(0, p - 1)
        #     v_layer[0] = self.create_v0(x[i_x])
        #     #propagamos entrada hasta a capa de salida
        #     for i in range(len(layers)-1):
        #         i+=1
        #         for j in range(layers[i]):
        #             v_layer[i][j] = self.calculate_v(v_layer[i-1], w[i][j], b)
        #
        #     # #delta para capa de salida
        #     last_pos = len(v_layer) - 1
        #     for i in range(len(h[last_pos])):
        #         h[last_pos][i] = self.calculate_h(w[last_pos][i],v_layer[last_pos])
        #         d[last_pos][i] = tanh_der(h[last_pos][i], b) * (y[last_pos] - v_layer[last_pos])
        #     # #retropropagamos delta
        #
        #     for i in range(len(v_layer)): #for para layers
        #         sum = 0
        #         for j in range(len(v_layer[i])-1):
        #             h[len(v_layer)-1-i][j] = self.calculate_h(w[len(v_layer)-1-i][j], v_layer[len(v_layer)-1-i])
        #             sum += w[len(v_layer)-1-i][j] * d[len(v_layer)-1-i][j]
        #         for j in range(len(v_layer[i])-1):
        #             d[len(v_layer)-1-i][j] = tanh_der(h[len(v_layer)-1-i][j],b) * sum
        #
        #     #actualizamos pesos
        #     for i in range(len(v_layer)-1):
        #         i+=1
        #         for j in range(len(v_layer[i-1]) - 1):
        #             delta_w = n * d[i][j] * v_layer[i-1][j]
        #             w[i][j] = w[i][j] + delta_w
        #
        #     print(w)
        b: float = 0.05
        p: int = len(y)
        #todo acordarse que la primera capa tiene que ser del tamaño de la entrada
        layers: list = [3, 4, 2]
        error = 1
        len_layers = len(layers)
        perceptrons = [None] * len_layers

        for i in range(len_layers):
            perceptrons[i] = [None] * layers[i]
            for j in range(layers[i]):
                perceptrons[i][j] = Perceptron(None, None, None, None)
                if i != len_layers-1: #si no es la ultima capa
                    perceptrons[i][j].w = [0] * layers[i+1]
                    for w in range(layers[i+1]):
                        perceptrons[i][j].w[w] = random.random()

        while error > MIN_ERROR:
            i_x = random.randint(0, p - 1)
            # aplicamos entrada a capa 0
            for j in range(layers[0]):
                perceptrons[0][j].v = x[i_x][j]

            print(perceptrons)
            # propagamos entrada hasta a capa de salida
            for i in range(len_layers):
                i+=1
                for j in range(layers[i]):
                    perceptrons[i][j].v = self.calculate_v(perceptrons[i-1][j].v,perceptrons[i][j].w,b)

            error = MIN_ERROR




    def calculate_v(self, v, w, b):
        h = self.calculate_h(w, v)
        return tanh(h, b)

    def create_v0(self, x_i_x):
        v0 = [0] * len(x_i_x)
        for i in range(len(x_i_x)):
            v0[i] = x_i_x[i]
        return v0

    def calculate_h(self, w, v):
        h: float = 0
        for j in range(len(v)):
            h += v[j]*w
        return h
