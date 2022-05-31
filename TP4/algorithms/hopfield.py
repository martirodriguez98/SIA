import math

from numpy import zeros, matmul, sign
from numpy.core import array_equal
import numpy as np

class Hopfield:
    def __init__(self, patterns,dataset):
        self.patterns = patterns
        self.dataset = dataset
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
            self.print_pattern(s2,5)
            if array_equal(s1,s2):
                convergence = True
            s1 = s2

        return self.results

    def orthogonal(self,p1,p2):
        o = 0
        for i in range(len(p1)):
            for j in range(i + 1, len(p1)):
                print(f"{self.letter_is(p2[i])} & {self.letter_is(p2[j])}: {np.inner(p1[i], p1[j])}")
                o += abs(np.inner(p1[i], p1[j]))
        return o/math.factorial(len(p1)-1)
    def letter_is(self, pattern):
        for l in range(len(self.dataset)):
            if (np.array(pattern) == np.array(self.dataset[l])).all():
                return chr(ord('A')+l)

    def print_pattern(self,pattern, length):
        mat = pattern.reshape(length, length)
        # print(mat)
        fmt = "".join(["{}" for i in range(length)])

        def pattern_mapper(x):
            if (x == 1):
                return "*"
            return " "

        print("-------------------------------\n")
        for i in range(length):
            print(fmt.format(*list(map(lambda x: pattern_mapper(x), mat[i]))))