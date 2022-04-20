import numpy as np
import matplotlib.pyplot as plt


def plot(plot_info: dict):
    x = [-1, 1, -1, 1]
    y = [1, -1, -1, 1]

    plt.plot(x, y, 'go')
    print(len(x))

    plt.xlim(-2, 2)
    plt.ylim(-2, 2)

    plt.axhline(0, color="black")
    plt.axvline(0, color="black")

    plt.plot(plot_info["x"][0], plot_info["y"][0])

    plt.show()
