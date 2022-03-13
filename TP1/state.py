from enum import Enum
from typing import List
import numpy as np


class Direction(Enum):
    LEFT = [0, -1]
    RIGHT = [0, 1]
    UP = [-1, 0]
    DOWN = [1, 0]

    def get_new_pos(self, pos: [int, int]) -> [int, int]:
        new_pos: [int, int] = (pos[0] + self.value[0], pos[1] + self.value[1])
        return new_pos


class State:
    def __init__(self, puzzle: np.array, empty_box: [int, int]):
        self.puzzle: np.array = puzzle
        self.empty_box: [int, int] = empty_box

    def valid_move(self, move_dir: Direction) -> bool:
        pos: [int, int] = move_dir.get_new_pos(self.empty_box)
        if pos[0] < 0 or pos[0] > 2 or pos[1] < 0 or pos[1] > 2:  # check if position is out of limits
            return False
        return True

    def get_valid_moves(self) -> List[Direction]:
        return list(filter(self.valid_move, Direction))

    def move_empty_box(self, move: Direction) -> 'State':
        if not self.valid_move(move):
            raise RuntimeError(f'Illegal player move {move}')

        old_empty_box: [int, int] = self.empty_box
        new_empty_box: [int, int] = move.get_new_pos(old_empty_box)
        puzzle: np.array = np.copy(self.puzzle)

        old_number: int = puzzle[new_empty_box[0]][new_empty_box[1]]
        puzzle[new_empty_box[0]][new_empty_box[1]] = 0
        puzzle[old_empty_box[0]][old_empty_box[1]] = old_number

        return State(puzzle, new_empty_box)

    def copy(self):
        return State(np.array(self.puzzle), self.empty_box)

    def __repr__(self) -> str:
        return f'{self.puzzle}\n'

    def __eq__(self, other):
        return isinstance(other, State) and np.array_equal(self.puzzle, other.puzzle)

    def __hash__(self):
        return hash((self.puzzle.data.tobytes()))
