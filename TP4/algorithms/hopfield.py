import copy

from numpy import zeros, matmul, ones, fill_diagonal, sign
from numpy.core import array_equal


class Hopfield:
    def __init__(self, patterns):
        self.patterns = patterns
        self.N = len(self.patterns[0])
        self.p = len(self.patterns)
        self.w = zeros((self.N,self.N))
        self.results = []
        for i in range(len(self.w)):
            for j in range(len(self.w[i])):
                if i == j:
                    self.w[i][j] = 0
                else:
                    sum = 0
                    for u in range(self.p):
                        sum += self.patterns[u][i] * self.patterns[u][j]
                    self.w[i][j] = (1 / self.p) * sum

    def algorithm(self, pattern):
        s1 = pattern
        self.results.append(s1)
        convergence = False

        while not convergence:
            s2 = sign(matmul(self.w, s1))
            self.results.append(s2)
            if array_equal(s1,s2):
                convergence = True
            s1 = s2

        return self.results
