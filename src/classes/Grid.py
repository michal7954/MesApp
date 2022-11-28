from params.consts import nodeSize
from helpers.printTable import printTable


class Grid:
    nodesNumber = None
    elementsNumber = None
    nodes = []
    elements = []
    HG = []

    def print(self):
        print(f"Nodes number: {self.nodesNumber}")

        print("Nodes:")
        for node in self.nodes:
            print(node)

        print()
        print(f"Elements number: {self.elementsNumber}")
        print("Elements:")
        for element in self.elements:
            print(element)

    def calculateHG(self):
        self.HG = [[0 for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]

        for element in self.elements:
            for i in range(nodeSize):
                for j in range(nodeSize):
                    self.HG[element.nodes[i].id - 1][element.nodes[j].id - 1] += element.HTotal[i][j]

    def printHG(self):
        print("HG Matrix")
        printTable(self.HG, 8, 2)
        print()
