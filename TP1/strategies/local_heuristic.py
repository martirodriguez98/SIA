from collections import deque
from typing import Collection, Set, Deque, Callable

from TP1.config_loader import StrategyParams
from TP1.heuristic import get_heuristic, get_heuristic_from_params
from TP1.node import Node, CostNode
from TP1.state import State


def local_heuristic(init_state: State, strategy_params: StrategyParams) -> Collection[State]:
    heuristic: Callable[[State], int] = get_heuristic_from_params(strategy_params)
    root = CostNode(init_state, None, heuristic)
    visited: Set[State] = set()
    visited.add(root.state)
    queue: Deque[CostNode] = deque()
    queue.append(root)

    while queue:
        current: CostNode = queue.pop()

        if current.puzzle_solved():
            return current.get_puzzle_solution()

        not_visited: set[CostNode] = set()

        for node in current.children():
            if node.state not in visited:
                not_visited.add(node)

        for node in not_visited:
            visited.add(node.state)
            queue.append(node)

    return []
