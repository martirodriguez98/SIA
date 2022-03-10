from enum import Enum
from typing import List, Iterator, Tuple


class Direction(Enum):
    UP = -3
    DOWN = 3
    LEFT = -1
    RIGHT = 1

    def get_new_pos(self, pos: int) -> int:
        new_pos: int = -1
        if (pos % 3 == 0 and self == Direction.LEFT ) or (pos % 3 == 1 and (self == Direction.DOWN) and pos != 4) or (pos % 3 == 2 and self == Direction.RIGHT):
            new_pos = pos + self.value
            if new_pos >= 0 and new_pos < 9:
                return new_pos
        return new_pos


class State:
    def __init__(self, puzzle: Tuple, empty_box: int):
        self.puzzle: Tuple = puzzle
        self.empty_box: int = empty_box

    def valid_move(self, move_dir: Direction) -> bool:
        pos: int = move_dir.get_new_pos(self.empty_box)
        if pos == -1:
            return False
        return True

    def get_valid_moves(self) -> Iterator[Direction]:
        return filter(self.valid_move, Direction)

    def move_empty_box(self, move: Direction) -> 'State':
        if not self.valid_move(move):
            raise RuntimeError(f'Illegal player move {move}')

        old_empty_box: int = self.empty_box

        new_state: State = self

        new_state.empty_box = move.get_new_pos(self.empty_box)

        old_number: int = new_state.puzzle[new_state.empty_box]

        aux_list = list(new_state.puzzle)
        aux_list[new_state.empty_box] = 0
        aux_list[old_empty_box] = old_number
        new_state.puzzle = tuple(aux_list)

        return new_state


    def copy(self):
        return State(self.puzzle, self.empty_box)

    def __repr__(self) -> str:
        return f'puzzle={self.puzzle}, empty_box={self.empty_box})'

    def __eq__(self, other):
        return self.puzzle == other.puzzle

    def __hash__(self):
        return hash((self.puzzle,self.empty_box))