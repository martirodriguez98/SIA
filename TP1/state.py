from enum import Enum
from typing import List, Iterator

class Direction(Enum):
    UP = (0,-1)
    DOWN = (0,1)
    LEFT = (-1,0)
    RIGHT = (1,0)

    def get_new_pos(self, pos: (int,int)) -> (int,int):
        new_pos: (int,int) = (pos[0] + self.value[0], pos[1] + self.value[1])
        return new_pos


class State:
    def __init__(self, puzzle: List[List[int]], empty_box: (int,int)):
        self.puzzle: List[List[int]] = puzzle
        self.empty_box: (int,int) = empty_box

    def valid_move(self, move_dir: Direction) -> bool:
        pos: (int,int) = move_dir.get_new_pos(self.empty_box)
        if pos[0] < 0 or pos[0] > 2 or pos[1] < 0 or pos[1] > 2: #check if position is out of limits
            return False
        return True

    def get_valid_moves(self) -> Iterator[Direction]:
        return filter(self.valid_move, Direction)

    def move_empty_box(self, move: Direction):
        if not self.valid_move(move):
            raise RuntimeError(f'Illegal player move {move}')

        old_empty_box: (int,int) = self.empty_box

        new_state: State = self.copy()

        new_state.empty_box = move.get_new_pos(new_state.empty_box)

        old_number: int = new_state.puzzle[new_state.empty_box[0]][new_state.empty_box[1]]
        new_state.puzzle[new_state.empty_box[0]][new_state.empty_box[1]] = 0
        new_state.puzzle[old_empty_box[0]][old_empty_box[1]] = old_number

        print(new_state.puzzle)
        return new_state


    def copy(self):
        return State(self.puzzle, self.empty_box)