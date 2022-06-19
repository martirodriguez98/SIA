import math

from numpy.random import uniform
from numpy import flip, array, mean, sum as npsum, concatenate, matmul, tanh
from scipy.optimize import minimize


class Autoencoder:

    def __init__(self, x, hidden_layers, latent_space, max_iter, min_error):
        self.iterations = 0
        self.x = x
        self.max_iter = max_iter
        self.min_error = min_error
        self.activation_fn = lambda h: tanh(h)
        self.latent_space = latent_space
        self.hidden_layers = hidden_layers
        self.network_layers = [len(x[0]), *hidden_layers, latent_space, *flip(hidden_layers), len(x[0])]
        self.dimensions = []
        self.w = []
        for i in range(len(self.network_layers)-1):
            self.dimensions.append((self.network_layers[i+1], self.network_layers[i]))
            self.w.append(uniform(low=-1, high=1, size=(self.network_layers[i + 1], self.network_layers[i])))

    def train(self):
        results = minimize(self.calculate_error,
                           self.w_vector(),
                           method="Powell",
                           callback=self.callback,
                           options={'xtol':self.min_error, 'maxiter': self.max_iter})
        print(self.propagate(self.w_matrix(results.x),self.x[0]))
        # print(self.x[0])

        return AEResults(self.iterations, self.w_matrix(results.x),results.fun)

    def calculate_error(self, w):
        o =[]
        weights = self.w_matrix(w)
        for v in self.x:
            o.append(self.propagate(weights, v))
        o = array(o)
        sum = npsum((self.x - o) ** 2,axis=1)
        return mean(sum / 2)

    def w_vector(self):
        w_vector = []
        for w in self.w:
            w_vector = concatenate((w_vector, w.flatten()))
        return w_vector

    def w_matrix(self, w):
        weights = []
        i = 0
        for d in self.dimensions:
            flat_dim = d[0] * d[1]
            weights.append(w[i: i + flat_dim].reshape(d))
            i += flat_dim
        return weights

    def propagate(self, weights, output):
        activation = output.reshape((len(output), 1))
        for layer in range(len(weights)):
            activation = self.activation_fn(matmul(weights[layer], activation))
        return activation.flatten()

    def callback(self,xk):
        self.iterations += 1
        print(f"iteration {self.iterations}")

    def encode(self, input_value, weights):
        return self.propagate(weights[:int(len(weights) / 2)], input_value)

    def decode(self, input_latent_value, weights):
        return self.propagate(weights[int(len(weights) / 2):], input_latent_value)

class AEResults:
    def __init__(self, iterations, weights, error):
        self.weights = weights
        self.iterations = iterations
        self.error = error