import heapq
from typing import Collection, Callable, Set

from config_loader import StrategyParams
from heuristic import get_heuristic_from_params
from node import CostNode
from state import State
from stats import Stats


def a_star(init_state: State, strategy_params: StrategyParams, stats: Stats) -> Collection[State]:
    heuristic: Callable[[State], int] = get_heuristic_from_params(strategy_params)
    root = CostNode(init_state, None, heuristic)
    visited: Set[State] = set()
    visited.add(root.state)
    queue: [CostNode] = [root]
    heapq.heapify(queue)

    while queue:
        current: CostNode = heapq.heappop(queue)
        stats.sum_cost(current.get_cost())
        if current.puzzle_solved():
            stats.set_result(True)
            stats.set_border_nodes_count(len(queue))
            return current.get_puzzle_solution()

        not_visited: set[CostNode] = set()

        for node in current.children():
            if node.state not in visited:
                not_visited.add(node)

        for node in not_visited:
            visited.add(node.state)
            heapq.heappush(queue, node)

        stats.sum_expanded_nodes()
    return []
