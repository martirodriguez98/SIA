from collections import deque
from typing import Collection, Set, Deque, Iterator

from TP1.node import Node
from TP1.state import State


def bpa(init_state: State) -> Collection[State]:
    root = Node(init_state, None)

    visited: Set[State] = set()
    visited.add(root.state)

    queue: Deque[Node] = deque()
    queue.append(root)

    while queue:
        current: Node = queue.popleft()
        if current.puzzle_solved():
            return current.get_puzzle_solution()

        not_visited: Iterator[Node] = filter(lambda node: node.state not in visited, current.children())

        for node in not_visited:
            visited.add(node.state)
            queue.append(node)
    return []
