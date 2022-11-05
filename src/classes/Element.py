import numpy as np
from classes.Elem4 import elem4
from configuration import pointsScheme
from consts import nodeSize

matrixSign = [
    [1, -1],
    [-1, 1]
]

class Element:
    id = None
    nodes = [None] * nodeSize
    matricesNumber = pointsScheme**2
    matrices = []

    def __init__(self, dataString) -> None:
        stringParts = dataString.split(', ')
        self.id = int(stringParts[0])
        nodes = stringParts[1:]
        for i in range(len(nodes)):
            nodes[i] = int(nodes[i])
        self.nodes = nodes
        # self.calculateMatrices()

    def __str__(self) -> str:
        stringNodesList = []
        for node in self.nodes:
            stringNodesList.append(node.id)
        return f'{self.id} -> {stringNodesList}'

    def calculateMatrices(self):
        # układ macierzy
        # [
        #     [dy/dEta, -dy/dKsi],
        #     [-dx/dEta, dx/dKsi],
        # ]
        matrix = [
            [0, 0],
            [0, 0]
        ]
        self.matrices = [matrix for _ in range(self.matricesNumber)]

        for point in range(self.matricesNumber):
            for i in range(2):
                for j in range(2):
                    self.matrices[point][i][j] = self.calculateValue(point, i, j)

        # self.printMatrices()
        

    def printMatrices(self):
        print('-----------------------------------')
        print('Element', self.id)
        for point in range(1):
            print(np.matrix(self.matrices[point]))
        print()

    def calculateValue(self, point, globalCoordsType, localCoordsType):
        sign = matrixSign[globalCoordsType][localCoordsType]
        globalCoords = []
        valuesList = None

        if globalCoordsType == 0:
            for i in range(nodeSize):
                globalCoords.append(self.nodes[i].y)
        elif globalCoordsType == 1:
            for i in range(nodeSize):
                globalCoords.append(self.nodes[i].x)

        if localCoordsType == 0:
            valuesList = elem4.dEta[point]
        elif localCoordsType == 1:
            valuesList = elem4.dKsi[point]

        sum = 0
        for i in range(nodeSize):
            sum += valuesList[i] * globalCoords[i]

        return sign * sum