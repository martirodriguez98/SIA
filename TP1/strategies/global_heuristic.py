import heapq
from typing import Collection, Set, Callable

from TP1.config_loader import StrategyParams
from TP1.heuristic import get_heuristic_from_params
from TP1.node import HeuristicNode
from TP1.state import State
from TP1.statistics import Statistics


def global_heuristic(init_state: State, strategy_params: StrategyParams, stats: Statistics) -> Collection[State]:
    heuristic: Callable[[State], int] = get_heuristic_from_params(strategy_params)
    root = HeuristicNode(init_state, None, heuristic)
    visited: Set[State] = set()
    visited.add(root.state)
    queue: [HeuristicNode] = [root]
    heapq.heapify(queue)

    while queue:
        current: HeuristicNode = heapq.heappop(queue)
        stats.sum_cost(current.heuristic_cost)
        if current.puzzle_solved():
            stats.set_result(True)
            stats.set_border_nodes_count(len(queue))
            return current.get_puzzle_solution()

        not_visited: set[HeuristicNode] = set()

        for node in current.children():
            if node.state not in visited:
                not_visited.add(node)

        for node in not_visited:
            visited.add(node.state)
            heapq.heappush(queue, node)

        stats.sum_expanded_nodes()

    return []