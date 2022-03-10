from collections import deque
from typing import Collection, Set, Deque, Iterator
import numpy as np
from TP1.node import Node
from TP1.state import State


def bpa(init_state: State) -> Collection[State]:
    root = Node(init_state, None)

    visited: Set[State] = set()
    visited.add(root.state)
    not_visited: Set[Node] = set()

    queue: Deque[Node] = deque()
    queue.append(root)

    while queue:
        print(f'Visited:')
        print(f' {visited}')
        print(f'Not visited: {not_visited}')
        current: Node = queue.popleft()
        if current.puzzle_solved():
            return current.get_puzzle_solution()

        # not_visited: Iterator[Node] = filter(lambda node: node.state in visited, current.children())
        print('children:')
        for n in current.children():
            print(n)


        for node in not_visited:
            visited.add(node.state)
            queue.append(node)

    return []
