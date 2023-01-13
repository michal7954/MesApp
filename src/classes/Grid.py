from params.consts import elementSize
from helpers.printTable import printTable
from numpy import linalg
from copy import deepcopy
from classes.Element import Element
from classes.Node import Node
from typing import MutableSequence


class Grid:
    nodesNumber = None
    elementsNumber = None
    nodes: MutableSequence[Node] = []
    elements: MutableSequence[Element] = []
    
    HG = []
    PG = []
    CG = []
    t = []

    def __init__(self, nodesList, elementsList, initialTemp):
        self.nodesNumber = len(nodesList)
        self.elementsNumber = len(elementsList)
        self.nodes = nodesList
        self.elements = elementsList
        self.t = [initialTemp for _ in range(self.nodesNumber)]

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

    # agregacja lokalnych macierzy H (z uwzględnionym warunkiem brzegowym) do globalnej H
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

    # agregacja lokalnych wektorów P do globalnego P
    def calculatePG(self):
        self.PG = [0 for _ in range(len(self.nodes))]
        for element in self.elements:
            for i in range(elementSize):
                self.PG[element.nodes[i].id - 1] += element.P[i]

    def printPG(self):
        print("PG Vector")
        print(self.PG)
        print()

    # agregacja lokalnych macierzy C do globalnej C
    def calculateCG(self):
        self.CG = [[0 for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]

        for element in self.elements:
            for i in range(elementSize):
                for j in range(elementSize):
                    self.CG[element.nodes[i].id - 1][element.nodes[j].id - 1] += element.C[i][j]

    def printCG(self):
        print("CG Matrix")
        printTable(self.CG, 8, 2)
        print()

    # symulacja pojedynczego kroku czasowego - wyznaczenie wektora temperatur po podanym czasie
    def simulate(self, simulationStepTime):
        H = deepcopy(self.HG)
        P = deepcopy(self.PG)

        # uwzględnienie macierzy C w macierzy H
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                H[i][j] += self.CG[i][j] / simulationStepTime

        # uwzględnienie macierzy C w wektorze P
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                P[i] += self.CG[i][j] * self.t[j] / simulationStepTime

        # print("H+C Matrix")
        # printTable(H, 10, 4)
        # print()

        # print("P+C Vector")
        # print(P)
        # print()

        # rozwiązanie układu równań z użyciem biblioteki numpy
        self.t = linalg.solve(H, P)

        # aktualizacja temperatury w węzłach
        for i in range(self.nodesNumber):
            self.nodes[i].temperature = self.t[i]

    def printSolution(self):
        print("Temperature Vector Solution")
        print(self.t)
        print()

    # wypisz minimalną i maksymalną temperaturę występującą w siatce w obecnej chwili symulacji
    def printSolutionMinMax(self, time):
        outputString = "{:3}".format(time)
        outputString += "{:14.6f}".format(min(self.t))
        outputString += "{:14.6f}".format(max(self.t))
        print(outputString)
