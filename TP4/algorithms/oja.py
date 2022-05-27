import numpy as np
from numpy.random import rand

class Oja:
    def __init__(self,x, learning_rate):
        self.learning_rate = learning_rate
        self.x = x
        self.N = len(x)
        self.n = len(x[0])
        self.w = rand(len(x[0]))*2 - 1
        self.epochs = 10000
        self.results = []

    def algorithm(self):
        self.results.append(self.w)

        for epoch in range(self.epochs):
            for i in range(self.N):
                s = self.x[i] @ self.w
                self.w = self.w + self.learning_rate * s * (self.x[i] - s * self.w)
                self.results.append(self.w)
        return self.results



