import heapq
from collections import deque
from typing import Collection, Set, Callable, Deque, List

from TP1.config_loader import StrategyParams
from TP1.heuristic import get_heuristic_from_params
from TP1.node import HeuristicNode
from TP1.state import State
from TP1.statistics import Statistics


def local_heuristic(init_state: State, strategy_params: StrategyParams, stats: Statistics) -> Collection[State]:
    heuristic: Callable[[State], int] = get_heuristic_from_params(strategy_params)
    root = HeuristicNode(init_state, None, heuristic)
    visited: Set[State] = set()
    visited.add(root.state)

    border_nodes: [HeuristicNode] = [root]
    heapq.heapify(border_nodes)

    while border_nodes:
        border_node: HeuristicNode = heapq.heappop(border_nodes)
        border_heuristic: int = border_node.heuristic_cost

        stack: Deque[HeuristicNode] = deque()
        stack.append(border_node)

        while stack:
            current_node: HeuristicNode = stack.pop()
            stats.sum_cost(current_node.heuristic_cost)
            if current_node.puzzle_solved():
                stats.set_result(True)
                stats.set_border_nodes_count(len(stack))
                return current_node.get_puzzle_solution()

            if current_node.heuristic_cost > border_heuristic:
                heapq.heappush(border_nodes, current_node)
                continue

            new_nodes: List[HeuristicNode] = []
            for n in current_node.children():
                if n.state not in visited:
                    new_nodes.append(n)

            for node in new_nodes:
                visited.add(node.state)
                stack.append(node)

            stats.sum_expanded_nodes()
    return []
