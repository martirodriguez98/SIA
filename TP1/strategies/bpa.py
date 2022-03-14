from collections import deque
from typing import Collection, Set, Deque

from config_loader import StrategyParams
from node import Node
from state import State
from stats import Stats


def bpa(init_state: State, strategy_params: StrategyParams, stats: Stats) -> Collection[State]:
    root = Node(init_state, None)
    visited: Set[State] = set()
    visited.add(root.state)

    queue: Deque[Node] = deque()
    queue.append(root)

    while queue:
        current: Node = queue.popleft()

        if current.puzzle_solved():
            stats.set_result(True)
            stats.set_border_nodes_count(len(queue))
            return current.get_puzzle_solution()

        not_visited: set[Node] = set()

        for node in current.children():
            if node.state not in visited:
                not_visited.add(node)

        for node in not_visited:
            visited.add(node.state)
            queue.append(node)

        stats.sum_expanded_nodes()
    return []
