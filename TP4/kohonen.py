import math
import random
from copy import copy
from numpy import average
import numpy as np

class Kohonen:
    def __init__(self, k, x, learning_rate, r):
        self.k = k
        self.x = x
        self.learning_rate = learning_rate
        self.r = r
        self.n = len(x[0])
        self.p = len(x)
        self.w = np.zeros((self.k,self.k,self.n))
        self.iterations = 500 * self.n
        self.set_weights()

#todo recordar que n < 1
    def algorithm(self):
        for t in range(self.iterations):
            rand = random.randint(0, self.p - 1)  # elijo una entrada de manera random
            min_i,min_j = self.find_winner_neuron(self.x[rand])
            for i in range(self.k):
                for j in range(self.k):
                    if self.is_neighbour(min_i,min_j,i,j):
                        self.w[i][j] = self.w[i][j] + self.learning_rate * (self.x[rand] - self.w[i][j])
            #todo check
            if t != 0:
                self.learning_rate = 1/t

    def set_weights(self):
        for i in range(self.k):
            for j in range(self.k):
                rand = random.randint(0, self.p - 1) #elijo una entrada de manera random
                self.w[i][j] = copy(self.x[rand])

    def find_winner_neuron(self, input):
        min_dist = self.euclidean_dist(self.w[0][0],input)
        min_i = 0
        min_j = 0
        for i in range(self.k):
            for j in range(self.k):
                for k in range(self.n):
                    euclidean_dist = self.euclidean_dist(self.w[i][j],input)
                    if euclidean_dist < min_dist:
                        min_i = i
                        min_j = j
        return min_i, min_j

    def euclidean_dist(self, w, x):
        sum = 0
        for i in range(len(w)):
            sum += (w[i] - x[i]) ** 2
        return math.sqrt(sum)

#todo check
    def is_neighbour(self,min_i, min_j, i, j):
        return self.euclidean_dist((min_i,min_j),(i,j)) <= self.r

    def get_neighbours_avg(self, neuron_i, neuron_j):
        euc_distance = []
        for i in range(self.k):
            for j in range(self.k):
                if self.is_neighbour(neuron_i,neuron_j,i,j):
                    euc_distance.append(euc_distance(self.w[i][j],self.w[neuron_i][neuron_j]))
        return average(euc_distance)


