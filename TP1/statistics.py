from typing import Optional, Collection
from TP1.config_loader import Config, StrategyParams
from TP1.state import State


class Statistics:
    def __init__(self, config_file: Config):
        self.strategy: str = config_file.strategy
        self.strategy_params: StrategyParams = config_file.strategy_params
        self.depth: int = 0
        self.cost: Optional[int] = None
        self.result: bool = False
        self.expanded_nodes_count: Optional[int] = None
        self.border_nodes_count: Optional[int] = None
        self.states: Collection[State] = []
        self.process_time: Optional[float] = None

    def set_depth(self, depth: int):
        self.depth = depth

    def set_result(self, result: bool):
        self.result = result

    def set_border_nodes_count(self, border_nodes_count: int):
        self.border_nodes_count = border_nodes_count

    def set_states(self, states: Collection[State]):
        self.states = states

    def set_process_time(self, start: float, end: float):
        self.process_time = end - start

    def sum_expanded_nodes(self):
        if self.expanded_nodes_count is not None:
            self.expanded_nodes_count += 1
        else:
            self.expanded_nodes_count = 1

    def sum_cost(self, cost: int):
        if self.cost is not None:
            self.cost += cost
        else:
            self.cost = cost

    def print_stats(self):
        if self.result:
            aux = "puzzle solved successfully!"
        else:
            aux = "couldn't solve puzzle"

        print('*' * 50)
        print(f'Statistics')
        print('*' * 50)
        print(f'Strategy: {self.strategy}\n'
          f'Strategy parameters: {self.strategy_params}\n'
          f'Depth: {self.depth}\n'
          f'Cost: {self.cost}\n'
          f'Result: {aux}\n'
          f'Total expanded nodes: {self.expanded_nodes_count}\n'
          f'Total border nodes: {self.border_nodes_count}\n'
          f'Process time: {self.process_time} seconds')
        print('*' * 50)
