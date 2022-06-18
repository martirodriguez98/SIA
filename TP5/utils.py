from typing import List

import numpy as np
from matplotlib import pyplot as plt


def transform_input(values: np.ndarray) -> np.ndarray:
    new_values = np.empty((np.size(values, 0), np.size(values, 1) * 5)).astype(int)
    for i in range(np.size(values,0)):
        total_bits: list = []
        for j in range(np.size(values,1)):
            binary_value = bin(values[i][j])[2:].zfill(5)
            total_bits.append(list(binary_value))
        new_values[i] = np.array(total_bits).flatten()
    return new_values

def print_bit_array(bit_array: List[float]):

    number: str = ''
    lines = 0
    for i, bit in enumerate(bit_array):
        if lines == 7:
            number += '\n\n'
            lines = 0
        if i != 0 and i % 5 == 0:
            number += '\n'
            lines+=1
        if float(bit) <= 0 or float(bit) < 0.5:
            number += ' '
        else:
            number += '*'
    print(number)


def labeled_scatter(x_values, y_values, labels=None):
    print(labels)
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.scatter(x_values, y_values, color='lightgreen')
    for l in range(len(labels)):
        plt.annotate(labels[l], (x_values[l],y_values[l]))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Representación de letras en el estado latente")
    plt.grid()
    plt.plot()
    plt.show()


