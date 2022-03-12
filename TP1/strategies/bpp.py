from collections import deque
from typing import Collection, Set, Deque

from TP1.node import Node
from TP1.state import State


def bpp(init_state: State) -> Collection[State]:
    root = Node(init_state, None)
    visited: Set[State] = set()
    visited.add(root.state)

    queue: Deque[Node] = deque()
    queue.append(root)

    while queue:
        current: Node = queue.pop()

        if current.puzzle_solved():
            return current.get_puzzle_solution()

        not_visited: set[Node] = set()
        for node in current.children():
            if node.state not in visited:
                not_visited.add(node)

        for node in not_visited:
            visited.add(node.state)
            queue.append(node)

    return []

#
# def dfs_iterative(graph, start):
#     stack, path = [start], []
#
#     while stack:
#         vertex = stack.pop()
#         if vertex in path:
#             continue
#         path.append(vertex)
#         for neighbor in graph[vertex]:
#             stack.append(neighbor)
#
#     return path
