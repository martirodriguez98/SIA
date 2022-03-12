from collections import deque
from typing import Optional, Collection, Deque, Iterator, List, Callable

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
            for y in range(len(self.state.puzzle)):
                if self.state.puzzle[x][y] != (3 * x + y + 1) and self.state.puzzle[x][y] != 0:
                    return False
        print('solved')
        return True

    def get_puzzle_solution(self) -> Collection[State]:
        state_queue: Deque[State] = deque()
        current: Optional[Node] = self
        while current:
            state_queue.appendleft(current.state)
            current = current.parent
        return state_queue

    def get_valid_states(self) -> List[State]:
        return list(map(lambda pos: self.state.move_empty_box(pos), self.state.get_valid_moves()))

    def children(self) -> List['Node']:
        return list(map(lambda state: Node(state, self), self.get_valid_states()))

    def __repr__(self) -> str:
        return f'Node(state={repr(self.state)}\n parent_id={id(self.parent)})'


class CostNode(Node):
    def __init__(self, state: State, parent: Optional['CostNode'], heuristic: Callable[[State], int]):
        super().__init__(state, parent)
        self.heuristic = heuristic
        self.heuristic_cost = self.heuristic(self.state)

    def children(self) -> List['CostNode']:
        return list(map(lambda state: type(self)(state, self, self.heuristic), self.get_valid_states()))

    def __repr__(self) -> str:
        return f'CosNode(state={repr(self.state)}\n parent_id={id(self.parent)})'
