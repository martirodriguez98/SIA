import random
from abc import ABC
from plot import plot_2d, plot_3d
import numpy as np

# chequear si la tenemos que definir nosotras o la pasan como parametro
COTA = 10
n = 0.01


class NeuralNetworkConfig:
    def __init__(self):
        self.x_count: int = 0
        self.neural: str
        self.single: str
        self.simple: str


class NeuralNetwork(ABC):
    def __init__(self, config_neural: NeuralNetworkConfig):
        self.config_neural: NeuralNetworkConfig = config_neural
        self.plot = {"x": [], "y": []}

    def train(self, x: np.ndarray, y: np.ndarray):
        pass

    def calculate_error(self, x: np.ndarray, y: np.ndarray, w: np.array, p: int):
        pass


class SimpleNeuralNetwork(NeuralNetwork):

    def train(self, x: np.ndarray, y: np.ndarray):
        p: int = len(y)
        i: int = 0
        w = np.zeros(self.config_neural.x_count)
        w_min = w
        error: int = 1
        error_min = p * 2
        while error > 0 and i < COTA:
            i_x = random.randint(0, p - 1)
            h = np.dot(x[i_x], w)
            o = np.copysign(1, h)
            delta_w = n * (y[i_x] - o) * x[i_x]
            w = w + delta_w
            error = self.calculate_error(x, y, w, p)
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
        error: int = 1
        error_min = p * 2
        while error > 0 and i < COTA:
            i_x = random.randint(0, p - 1)
            h = np.dot(x[i_x], w)
            o = self.activation(w, x)
            delta_w = n * (y[i_x] - o) * x[i_x]
            w = w + delta_w
            error = self.calculate_error(x, y, w, p)
            if error < error_min:
                error_min = error
                w_min = w
            i = i + 1
        self.plot["x"].append(np.arange(-2, 4))
        self.plot["y"].append((-w_min[1] / w_min[2]) * np.arange(-2, 4) - w_min[0] / w_min[2])
        plot_3d(self.plot, x, y)

    def activation(self, w: np.array, x: np.ndarray):
        o: float = 0
        for i in range(self.config_neural.x_count):
            o += sum(w[i] * x[i])
        return o

    def calculate_error(self, x: np.ndarray, y: np.ndarray, w: np.array, p: int):
        o = []
        for i in range(p):
            o.append(0.5 * pow(abs(y[i] - np.copysign(1, np.dot(x[i], w))), 2))
        return sum(o)

# class NonLinearNeuralNetwork(SingleNeuralNetwork):
#     #extiende a SingleNeuralN
#
#
# class MultilayerNeuralNetwork(NeuralNetwork):
#     #clase (no abs) para el multicapa (ej 3)
