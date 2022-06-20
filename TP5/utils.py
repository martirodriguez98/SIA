from typing import List
import plotly.graph_objects as go

import numpy as np
from matplotlib import pyplot as plt
from numpy import flip, reshape, random, array
from plotly.subplots import make_subplots


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

def letter_heatmap(font):
    fig = make_subplots(rows=4, cols=8)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    row = 1
    col = 1

    for v in font:
        if col == 9:
            col = 1
            row += 1

        fig.add_heatmap(
            z = flip(reshape(v, (7,5)), axis=0),
            showscale=False,
            row=row,
            col=col,
            colorscale='Greys',
            colorbar=dict(bordercolor="black", borderwidth=1)
        )
        col += 1
    fig.show()

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

def latent_layer_plot(values, letters):
    fig = go.Figure(
        data = [
            go.Scatter(
                x=values[:,0],
                y=values[:,1],
                text=letters,
                mode='markers'
            )
        ],
        layout=go.Layout(
            title="Latent Space",
            xaxis=dict(title="x"),
            yaxis=dict(title="y"),
        )
    )
    for i in range(len(values)):
        fig.add_annotation(
            x=values[i, 0],
            y=values[i, 1],
            ax=0, ay=0,
            xanchor="center",
            yanchor="bottom",
            text=letters[i],
            font=dict(size=18)
        )
    fig.update_traces(textposition='top center')
    fig.show()

def add_noise(set):
    new_set = []
    for s in set:
        element = []
        for e in s:
            r = random.uniform()
            if r <= 0.15:
                if e == 1:
                    element.append(e - r * 10)
                else:
                    element.append(e + r * 10)
            else:
                element.append(e)
        new_set.append(element)
    return array(new_set)

