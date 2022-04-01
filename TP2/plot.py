import numpy as np
import matplotlib.pyplot as plt


def plot(plot_info: dict, title: str):
    x = np.array(range(len(plot_info["min_fitness"])))

    fig, ax = plt.subplots(figsize=(10, 8), layout="constrained")

    ax.set_xlabel("Generation", fontsize=15)
    ax.set_ylabel("Fitness", fontsize=15)
    plt.xlim(0, 1000)
    plt.ylim(0, 9000)
    ax.locator_params("y", nbins=10)
    ax.locator_params("x", nbins=10)
    ax.plot(x, plot_info["min_fitness"], label="Min fitness", color="r")
    ax.plot(x, plot_info["max_fitness"], label="Max fitness", color="b")
    ax.plot(x, plot_info["avg_fitness"], label="Avg fitness", color="y")
    ax.set_title(title, fontsize=15)
    ax.legend(prop={"size": 20})
    plt.show()
