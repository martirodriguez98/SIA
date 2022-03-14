from collections import deque
from functools import total_ordering
from typing import Optional, Collection, Deque, List, Callable

from state import State


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

    def __eq__(self, other):
        return isinstance(other,Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def __repr__(self) -> str:
        return f'Node(state={repr(self.state)}\n parent_id={id(self.parent)})'


class HeuristicNode(Node):
    def __init__(self, state: State, parent: Optional['HeuristicNode'], heuristic: Callable[[State], int]):
        super().__init__(state, parent)
        self.heuristic = heuristic
        self.heuristic_cost: int = self.heuristic(self.state)

    def children(self) -> List['HeuristicNode']:
        return list(map(lambda state: type(self)(state, self, self.heuristic), self.get_valid_states()))

    def __repr__(self) -> str:
        return f'CosNode(state={repr(self.state)}\n parent_id={id(self.parent)})'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, HeuristicNode):
            return False
        return self.heuristic_cost == o.heuristic_cost and self.state == o.state

    def __hash__(self) -> int:
        return hash((self.heuristic_cost,hash(self.state)))

    @total_ordering
    def __lt__(self, other: 'HeuristicNode') -> bool:
        return self.heuristic_cost < other.heuristic_cost


class CostNode(HeuristicNode):
    def get_cost(self):
        return self.heuristic_cost + self.depth

    def children(self) -> List['CostNode']:
        return list(map(lambda state: type(self)(state, self, self.heuristic), self.get_valid_states()))

    def __eq__(self, other):
        if not isinstance(other, CostNode):
            return False
        return self.depth == other.depth and self.get_cost() == other.get_cost() and self.state == other.state

    def __hash__(self) -> int:
        return hash((self.heuristic_cost, self.depth,self.state))

    @total_ordering
    def __lt__(self, other: 'CostNode') -> bool:
        equal_cost: bool = self.get_cost() == other.get_cost()
        if equal_cost:
            return self.heuristic_cost < other.heuristic_cost
        else:
            return self.get_cost() < other.get_cost()
