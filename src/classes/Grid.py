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
    CG = []
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
        print("PG Vector")
        print(self.PG)
        print()

    def calculateAgregateCG(self, simulationStepTime, initialTemp):
        self.CG = [[0 for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]

        for element in self.elements:
            for i in range(elementSize):
                for j in range(elementSize):
                    self.CG[element.nodes[i].id - 1][element.nodes[j].id - 1] += element.C[i][j]

        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                self.HG[i][j] += self.CG[i][j] / simulationStepTime

        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                self.PG[i] += self.CG[i][j] / simulationStepTime * initialTemp

    def printCG(self):
        print("CG Matrix")
        printTable(self.CG, 8, 2)
        print()

    def solve(self):
        self.t = linalg.solve(self.HG, self.PG)

    def printSolution(self):
        print("Temperature Vector Solution")
        print(self.t)
        print()
