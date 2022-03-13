from typing import List
from TP1.node import Node

import graphviz


class Graph:
    def __init__(self, node: Node):
        self.graph: List[Node] = [node]
        self.dot: graphviz.Digraph = graphviz.Digraph()

    def add_node(self, node: Node):
        self.graph.append(node)
        self.dot.node(node.state.__repr__())
        if node.parent is not None:
            self.dot.edges([node.parent.state.__repr__(), node.state.__repr__()])
