from collections import deque
from typing import Collection, Deque, Dict, List

from config_loader import StrategyParams
from node import Node
from state import State
from stats import Stats


def bppv(init_state: State, strategy_params: StrategyParams, stats: Stats) -> Collection[State]:
    step: int = (strategy_params.get('step', 10) if strategy_params else 20)

    root: Node = Node(init_state, None)

    stack: Deque[Node] = deque()

    border_nodes: Deque[Node] = deque()  #border nodes

    border_nodes.append(root)

    # when a state is reached, its depth is saved so if its found again it can decide if its worth exploring
    visited_states_depth: Dict[State, int] = dict()
    visited_states_depth[root.state] = 0

    while border_nodes:
        node: Node = border_nodes.popleft()

        max_depth: int = node.depth + step
        stack.append(node)

        while stack:
            current_node: Node = stack.pop()

            if current_node.depth >= max_depth:
                border_nodes.append(current_node)
                continue

            if current_node.puzzle_solved():
                stats.set_result(True)
                stats.set_border_nodes_count(len(stack))
                return current_node.get_puzzle_solution()

            new_nodes: List[Node] = []
            for n in current_node.children():
                if n.state not in visited_states_depth.keys() or n.depth < visited_states_depth[n.state]:
                    new_nodes.append(n)

            for new_node in new_nodes:
                visited_states_depth[new_node.state] = new_node.depth
                stack.append(new_node)

            stats.sum_expanded_nodes()
    return []
