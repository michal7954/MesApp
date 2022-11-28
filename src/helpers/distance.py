from math import sqrt
from classes.Node import Node


def distance(nodeA: Node, nodeB: Node) -> float:
    return sqrt((nodeA.x - nodeB.x) ** 2 + (nodeA.y - nodeB.y) ** 2)
