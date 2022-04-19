import numpy as np
import matplotlib.pyplot as plt


def plot(all_w: list):
    x = [-1, 1, -1, 1]
    y = [1, -1, -1, 1]
    print(all_w)
    # x.append(w[1])
    # y.append(w[2])
    x_w = []
    y_w = []
    for e in all_w:
        x_w.append(e[1])
        y_w.append(e[2])

    plt.axhline(0,color="black")
    plt.axvline(0,color="black")
    plt.scatter(x,y)
    plt.scatter(x_w,y_w)
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.title("Points")
    plt.show()