from params.consts import elementSize
from helpers.printTable import printTable
from numpy import linalg


class Grid:
    nodesNumber = None
    elementsNumber = None
    nodes = []
    elements = []
    HG = []
    PG = []
    t = []

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
            for i in range(elementSize):
                for j in range(elementSize):
                    self.HG[element.nodes[i].id - 1][element.nodes[j].id - 1] += element.HTotal[i][j]

    def printHG(self):
        print("HG Matrix")
        printTable(self.HG, 8, 2)
        print()

    def calculatePG(self):
        self.PG = [0 for _ in range(len(self.nodes))]
        for element in self.elements:
            for i in range(elementSize):
                self.PG[element.nodes[i].id - 1] += element.P[i]

    def printPG(self):
        print(self.PG)

    def solve(self):
        self.t = linalg.solve(self.HG, self.PG)

    def printSolution(self):
        print(self.t)
