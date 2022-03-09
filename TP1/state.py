from typing import List

class State:
    def __init__(self, puzzle: List[List[int]], empty_box_x: int, empty_box_y: int):
        self.puzzle: List[List[int]] = puzzle
        self.empty_box_x: int = empty_box_x
        self.empty_box_y: int = empty_box_y

