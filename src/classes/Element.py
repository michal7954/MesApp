import numpy as np
from copy import deepcopy
from classes.Elem4 import elem4
from params.configuration import pointsScheme
from params.consts import nodeSize

class Element:
    id = None
    nodes = [None] * nodeSize
    matricesNumber = pointsScheme**2
    jacobianMatrices = []
    jacobianDeterminants = []
    invertibleJacobianMatrices = []

    def __init__(self, dataString) -> None:
        stringParts = dataString.split(', ')
        self.id = int(stringParts[0])
        nodes = stringParts[1:]
        for i in range(len(nodes)):
            nodes[i] = int(nodes[i])
        self.nodes = nodes

    def __str__(self) -> str:
        stringNodesList = []
        for node in self.nodes:
            stringNodesList.append(node.id)
        return f'{self.id} -> {stringNodesList}'

    def calculateMatrices(self):
        templateMatrix = [
            [0, 0],
            [0, 0]
        ]
        self.jacobianMatrices = [deepcopy(templateMatrix) for _ in range(self.matricesNumber)]
        self.jacobianDeterminants = [0 for _ in range(self.matricesNumber)]
        self.invertibleJacobianMatrices = [deepcopy(templateMatrix) for _ in range(self.matricesNumber)]

        for point in range(self.matricesNumber):
            for i in range(2):
                for j in range(2):
                    self.jacobianMatrices[point][i][j] = self.calculateValue(point, i, j)

            self.jacobianDeterminants[point] = np.linalg.det(self.jacobianMatrices[point])

            # układ macierzy odwrotnej
            # [
            #     [dy/dEta, -dy/dKsi],
            #     [-dx/dEta, dx/dKsi],
            # ]
            self.invertibleJacobianMatrices[point][0][0] = self.jacobianMatrices[point][1][1] / self.jacobianDeterminants[point]
            self.invertibleJacobianMatrices[point][0][1] = -self.jacobianMatrices[point][0][1] / self.jacobianDeterminants[point]
            self.invertibleJacobianMatrices[point][1][0] = -self.jacobianMatrices[point][1][0] / self.jacobianDeterminants[point]
            self.invertibleJacobianMatrices[point][1][1] = self.jacobianMatrices[point][0][0] / self.jacobianDeterminants[point]
        

    def calculateValue(self, point, localCoordsType, globalCoordsType):
        globalCoords = []
        valuesList = None

        # wybranie odpowiednich współrzędnych do interpolacji (x lub y)
        if globalCoordsType == 0:
            for i in range(nodeSize):
                globalCoords.append(self.nodes[i].x)
        elif globalCoordsType == 1:
            for i in range(nodeSize):
                globalCoords.append(self.nodes[i].y)

        # wybranie wartości pochodnych po odpowiedniej współrzędnej lokalnej i dla odpowiedniego punktu całkowania
        if localCoordsType == 0:
            valuesList = elem4.dKsi[point]
        elif localCoordsType == 1:
            valuesList = elem4.dEta[point]

        # interpolacja elementu macierzy Jacobiego
        sum = 0
        for i in range(nodeSize):
            sum += valuesList[i] * globalCoords[i]

        return sum

    def printMatrices(self):
        outputJacobianTable = [[0 for _ in range(self.matricesNumber)] for _ in range(4)]
        outputInvertibleJacobianTable = [[0 for _ in range(self.matricesNumber)] for _ in range(4)]

        for point in range(self.matricesNumber):
            outputJacobianTable[0][point] = self.jacobianMatrices[point][0][0]
            outputJacobianTable[1][point] = self.jacobianMatrices[point][0][1]
            outputJacobianTable[2][point] = self.jacobianMatrices[point][1][0]
            outputJacobianTable[3][point] = self.jacobianMatrices[point][1][1]

            outputInvertibleJacobianTable[0][point] = self.invertibleJacobianMatrices[point][0][0]
            outputInvertibleJacobianTable[1][point] = self.invertibleJacobianMatrices[point][0][1]
            outputInvertibleJacobianTable[2][point] = self.invertibleJacobianMatrices[point][1][0]
            outputInvertibleJacobianTable[3][point] = self.invertibleJacobianMatrices[point][1][1]

        print('-----------------------------------')
        print('Element', self.id)
        print(np.matrix(outputJacobianTable))
        print()
        print(np.array(self.jacobianDeterminants))
        print()
        print(np.matrix(outputInvertibleJacobianTable))
        print()