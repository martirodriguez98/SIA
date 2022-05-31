from numpy.random import rand
import matplotlib.pyplot as plt
import numpy as np

class Oja:
    def __init__(self,x, learning_rate):
        self.learning_rate = learning_rate
        self.x = x
        self.N = len(x)
        self.n = len(x[0])
        self.w = rand(self.n)*2 - 1
        self.epochs = 1000
        self.results = []

    def algorithm(self):
        self.results.append(self.w)

        for epoch in range(self.epochs):
            for i in range(self.N):
                s = self.x[i] @ self.w
                self.w = self.w + self.learning_rate * s * (self.x[i] - s * self.w)
                self.results.append(self.w)
        return self.results

    def reset(self):
        self.w = rand(self.n) * 2 - 1
        self.results = []

    def plot(self, x_axis, y_axis,x_label,y_label,title,figsize,decimals ):
        plt.figure(figsize=figsize)
        hbar = plt.barh(x_axis,y_axis,color=self.bar_color(y_axis,'#d396ec', '#c7d566'))
        # hbar = plt.barh(x_axis, y_axis, color=self.bar_color(y_axis, '#95d7dd', '#ce6f67'))
        plt.title(title)
        plt.bar_label(hbar,fmt=decimals)
        plt.xticks(rotation=90)
        # plt.ylabel(y_label)
        # plt.xlabel(x_label)
        plt.show()

    def plot_errors(self, x_axis, y_axis,x_label,y_label,title,figsize,decimals ):
        plt.figure(figsize=figsize)
        hbar = plt.bar(x_axis,y_axis, color='#d396ec')
        plt.title(title)
        plt.bar_label(hbar,fmt=decimals)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.grid(axis='y')
        plt.show()

    def bar_color(self,data, color1, color2):
        return np.where(data > 0, color1, color2).T



