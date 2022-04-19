import numpy as np
import matplotlib.pyplot as plt


def plot(plot_info: dict):
    x = np.array([[1, -1, 1], [1, 1, -1], [1, -1, -1], [1, 1, 1]])
    y = np.array([-1, -1, -1, 1])

    fig, ax = plt.subplots(figsize=(10, 8), layout="constrained")

    ax.set_xlabel("x", fontsize=15)
    ax.set_ylabel("y", fontsize=15)
    plt.scatter(x, y)
    plt.xlim(0, 5)
    plt.ylim(0, 5)
    ax.locator_params("y", nbins=10)
    ax.locator_params("x", nbins=10)
    ax.plot(x, plot_info["x"], label="x", color="r")
    ax.plot(x, plot_info["y"], label="y", color="b")
    ax.legend(prop={"size": 20})
    plt.show()

    # def plot(all_w: list):
#     x = [-1, 1, -1, 1]
#     y = [1, -1, -1, 1]
#     print(all_w)
#     # x.append(w[1])
#     # y.append(w[2])
#     x_w = []
#     y_w = []
#     for e in all_w:
#         x_w.append(e[1])
#         y_w.append(e[2])
#
#     plt.axhline(0,color="black")
#     plt.axvline(0,color="black")
#     plt.scatter(x,y)
#     plt.scatter(x_w,y_w)
#     plt.xlabel("X")
#     plt.ylabel("Y")
#
#     plt.title("Points")
#     plt.show()
