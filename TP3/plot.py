from typing import List

import numpy as np
import matplotlib.pyplot as plt

from results import Results


def plot_2d(plot_info: dict, in_x: np.ndarray, in_y: np.ndarray):
    fig = plt.figure()
    ax = fig.add_subplot()
    pos_values_x: List = []
    pos_values_y: List = []
    neg_values_x: List = []
    neg_values_y: List = []

    for i in range(len(in_y)):
        if in_y[i] > 0:
            pos_values_x.append(in_x[i][1])
            pos_values_y.append(in_x[i][2])
        else:
            neg_values_x.append(in_x[i][1])
            neg_values_y.append(in_x[i][2])

    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    ax.scatter(pos_values_x, pos_values_y, color='red')
    ax.scatter(neg_values_x, neg_values_y, color='black')
    plt.axhline(0, color="black")
    plt.axvline(0, color="black")

    plt.plot(plot_info["x"][0], plot_info["y"][0], color='blue')

    plt.show()


def plot_errors(plot_info: dict, in_x: np.ndarray, in_y: np.ndarray):
    # fig = plt.figure()
    # ax = fig.add_subplot()
    x = []
    for i in range(len(plot_info["errors"])):
        x.append(i)
        print(f'error: {plot_info["errors"][i]}')
    # plt.set_xlabel('iteration')
    # plt.set_ylabel('error')
    # plt.scatter(x, plot_info["errors"], color='red')
    plt.plot(x,plot_info["errors"])
    plt.show()

def plot_prediction(predicted, expected, title, x_label, y_label):
    fig = plt.figure()
    ax = fig.add_subplot()
    x_values = range(0, len(expected))
    ax.scatter(x_values, expected, color='black')
    ax.scatter(x_values, predicted, color='blue')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()