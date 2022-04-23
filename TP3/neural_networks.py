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



class MultilayerNeuralNetwork(NeuralNetwork):
    def train(self, x: np.ndarray, y: np.ndarray):
        b: float = 0.05
        p: int = len(y)
        # conjunto de pesos en valores pequeñoas al azar
        w: np.ndarray = np.empty(len(x))
        for i in range(len(x)):
            w[i] = random.random()
        error: float = 1
        # TODO parametrizar
        layers: list = [3, 2, 4]
        v_layer: np.ndarray = [None] * len(layers)
        d: np.ndarray = np.empty(len(layers))
        for i in range(len(v_layer)):
            v_layer[i] = [None] * (layers[i])

        while error > MIN_ERROR:
            i_x = random.randint(0, p - 1)
            v = self.create_v0(x[i_x])
            #propagamos entrada hasta a capa de salida
            for i in layers:
                v = self.calculate_v(v, w, b)
            #delta para capa de salida
            last_pos = len(v_layer) - 1
            h = self.calculate_h(w,v)
            d[last_pos] = tanh_der(h, b) * (y[last_pos] - v[last_pos])
            #retropropagamos delta
            for i in range(len(d)-1):
                i+=1
                h = self.calculate_h(w,v)




    def calculate_v(self, v, w, b):
        h: float = self.calculate_h(w, v)
        v_new: np.ndarray = np.empty(len(v))
        for i in range(len(v)):
            v[i] = tanh(h, b)
        return v_new

    def create_v0(self, x_i_x):
        v0: np.ndarray = np.empty(len(x_i_x))
        for i in range(len(x_i_x)):
            v0[i] = x_i_x[i]
        return v0

    def calculate_h(self, w, v):
        h: float = 0
        for j in range(len(v)):
            h += v[j]*w[j]
        return h
