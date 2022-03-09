from collections import deque
from typing import Collection, Set, Deque

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


    #   # If not visited, mark it as visited, and
    #   # enqueue it
    #   for neighbour in graph[vertex]:
    #     if neighbour not in visited:
    #       visited.add(neighbour)
    #       queue.append(neighbour)

    return []
