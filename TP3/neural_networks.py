import random
from abc import ABC
from plot import plot_2d, plot_errors
from config import Param
import numpy as np
from typing import Callable

# chequear si la tenemos que definir nosotras o la pasan como parametro
COTA = 100
n = 0.001

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

    def calculate_delta_w(self,x: np.ndarray, y: np.ndarray, p: int, i_x: int, h: float,b: float):
        delta_w: float = 0
        for i in range(p):
            delta_w += (y[i_x] - tanh(h, b)) * tanh_der(h, b) * x[i_x]
        return n * delta_w

def tanh(x: float, b: float) -> float:
    return np.tanh(b * x)

def tanh_der(x: float, b: float) -> float:
    return b * (1 - tanh(x, b) ** 2)


# class MultilayerNeuralNetwork(NeuralNetwork):
#     #clase (no abs) para el multicapa (ej 3)
