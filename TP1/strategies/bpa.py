from collections import deque
from typing import Collection, Set, Deque, Iterator
import numpy as np

from TP1.config_loader import StrategyParams
from TP1.node import Node
from TP1.state import State


def bpa(init_state: State, strategy_params: StrategyParams) -> Collection[State]:
    root = Node(init_state, None)

    # visited: Set[State] = set()
    # visited.add(root.state)
    visited: Set[State] = set()
    visited.add(root.state)

    queue: Deque[Node] = deque()
    queue.append(root)

    while queue:
        # print(f'Visited:')
        # print(f' {visited}')

        current: Node = queue.popleft()

        if current.puzzle_solved():
            return current.get_puzzle_solution()

        # not_visited: Iterator[Node] = filter(lambda node: node.state not in visited, current.children())
        not_visited: set[Node] = set()

        for node in current.children():
            # print(node)
            if node.state not in visited:
                not_visited.add(node)

        for node in not_visited:
            visited.add(node.state)
            queue.append(node)

    return []
