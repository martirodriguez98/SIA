from typing import List, Tuple

import numpy as np


class Item:
    def __init__(self, benefit: int, weight: int):
        self.benefit: int = benefit
        self.weight: int = weight
        self.selected: int = 0
        self.fitness: float = self.benefit / self.weight

    def __repr__(self):
        return f'benefit: {self.benefit}, weight: {self.weight}'


def load_data(items_file: str) -> Tuple[int, int, List[Item]]:  # total_items,max_weight,items
    try:
        data = np.loadtxt(items_file, delimiter=' ', dtype=int)

        total_items: int = data[0][0]
        max_weight: int = data[0][1]
        items: List[Item] = []

        for index in range(len(data)):
            if index == 0:
                continue
            items.append(Item(data[index][0], data[index][1]))
        return total_items, max_weight, items

    except FileNotFoundError:
        raise FileNotFoundError(f'File {items_file} not found')
