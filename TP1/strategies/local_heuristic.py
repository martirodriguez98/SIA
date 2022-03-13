import heapq
from collections import deque
from typing import Collection, Set, Callable, Deque, List

from TP1.config_loader import StrategyParams
from TP1.heuristic import get_heuristic_from_params
from TP1.node import HeuristicNode
from TP1.state import State


def local_heuristic(init_state: State, strategy_params: StrategyParams) -> Collection[State]:
    heuristic: Callable[[State], int] = get_heuristic_from_params(strategy_params)
    root = HeuristicNode(init_state, None, heuristic)
    visited: Set[State] = set()
    visited.add(root.state)

    neighbour_nodes: [HeuristicNode] = [root]
    heapq.heapify(neighbour_nodes)

    while neighbour_nodes:
        neighbour_node: HeuristicNode = heapq.heappop(neighbour_nodes)
        neighbour_heuristic: int = neighbour_node.heuristic_cost

        stack: Deque[HeuristicNode] = deque()
        stack.append(neighbour_node)

        while stack:
            current_node: HeuristicNode = stack.pop()

            if current_node.puzzle_solved():
                return current_node.get_puzzle_solution()

            if current_node.heuristic_cost > neighbour_heuristic:
                heapq.heappush(neighbour_nodes, current_node)
                continue

            new_nodes: List[HeuristicNode] = []
            for n in current_node.children():
                if n.state not in visited:
                    new_nodes.append(n)

            for node in new_nodes:
                visited.add(node.state)
                stack.append(node)

    return []
