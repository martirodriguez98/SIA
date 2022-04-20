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
    a = np.array(plot_info["x"])
    b = np.array(plot_info["y"])
    print(a[0])
    print(b[0])
    plt.plot(a[0], b[0])

    plt.show()
