from typing import Set

import numpy as np

from config_loader import Config

class Item:
    def __init__(self, benefit: int, weight: int):
        self.benefit:int = benefit
        self.weight:int = weight
        self.selected: int = 0

    def __repr__(self):
        return f'benefit: {self.benefit}, weight: {self.weight}'

class Items:
    def __init__(self, items_file: str):
        try:
            data = np.loadtxt(items_file,delimiter=' ', dtype=int)
            self.total_items: int = data[0][0]
            self.max_weight: int = data[0][1]
            self.items: np.array = []

            for index in range(len(data)):
                if index == 0:
                    continue
                self.items.append(Item(data[index][0],data[index][1]))

        except FileNotFoundError:
            raise FileNotFoundError(f'File {items_file} not found')

