from collections import deque
from typing import Optional, Collection, Deque, Iterator

from TP1.state import State


class Node:

    def __init__(self, state: State, parent: Optional['Node']):
        self.state: State = state
        self.parent: Optional[Node] = parent
        self.depth: int
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

    def puzzle_solved(self) -> bool:
        for x in range(len(self.state.puzzle)):
            for y in range(len(self.state.puzzle[x])):
                if self.state.puzzle[x][y] != (3 * x + y + 1):
                    return False
        return True

    def get_puzzle_solution(self) -> Collection[State]:
        state_queue: Deque[State] = deque()
        current: Optional[Node] = self
        while current:
            state_queue.appendleft(current.state)
            current = current.parent

        return state_queue

    def children(self) -> Iterator['Node']:
        children_it: Iterator[State] = map(self.state.move_empty_box, self.state.get_valid_moves())
        return map(lambda state: Node(state,self), children_it)

    def __repr__(self) -> str:
        return f'Node(state={repr(self.state)}, parent_id={id(self.parent)})'