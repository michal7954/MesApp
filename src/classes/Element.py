import numpy as np
from copy import deepcopy
from classes.Elem4 import elem4
from params.configuration import pointsScheme
from params.consts import nodeSize
from helpers.generatePoints import weights

class Element:
    id = None
    nodes = [None] * nodeSize
    pointsNumber = pointsScheme**2

    jacobianMatrices = []
    jacobianDeterminants = []
    invertibleJacobianMatrices = []

    dx = []
    dy = []
    
    dxH = []
    dyH = []
    H = []
    HTotal = []

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

    # obliczenie macierzy Jakobiego, Jakobianu i odwrotnej macierzy Jakobiego w każdym punkcie całkowania
    def calculateJacobians(self):
        templateMatrix = [
            [0, 0],
            [0, 0]
        ]
        self.jacobianMatrices = [deepcopy(templateMatrix) for _ in range(self.pointsNumber)]
        self.jacobianDeterminants = [0 for _ in range(self.pointsNumber)]
        self.invertibleJacobianMatrices = [deepcopy(templateMatrix) for _ in range(self.pointsNumber)]

        for point in range(self.pointsNumber):
            for i in range(2):
                for j in range(2):
                    self.jacobianMatrices[point][i][j] = self.calculateJacobianElement(point, i, j)

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
        

    def calculateJacobianElement(self, point, localCoordsType, globalCoordsType):
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

    def printJacobians(self):
        outputJacobianTable = [[0 for _ in range(self.pointsNumber)] for _ in range(4)]
        outputInvertibleJacobianTable = [[0 for _ in range(self.pointsNumber)] for _ in range(4)]

        for point in range(self.pointsNumber):
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

    def calculateShapeFunctionsDerivates(self):
        self.dx = [[0 for _ in range(nodeSize)] for _ in range(self.pointsNumber)]
        self.dy = [[0 for _ in range(nodeSize)] for _ in range(self.pointsNumber)]

        for point in range(self.pointsNumber):
            for i in range(nodeSize):
                self.dx[point][i] = self.invertibleJacobianMatrices[point][0][0] * elem4.dKsi[point][i] + self.invertibleJacobianMatrices[point][0][1] * elem4.dEta[point][i]
                self.dy[point][i] = self.invertibleJacobianMatrices[point][1][0] * elem4.dKsi[point][i] + self.invertibleJacobianMatrices[point][1][1] * elem4.dEta[point][i] 

    def printShapeFuncitonsDerivates(self):
        print(np.matrix(self.dx))
        print()
        print(np.matrix(self.dy))
        print()

    def calculateH(self, conductivity):
        templateMatrix = [[0 for _ in range(nodeSize)] for _ in range(nodeSize)]

        self.dxH = [deepcopy(templateMatrix) for _ in range(self.pointsNumber)]
        self.dyH = [deepcopy(templateMatrix) for _ in range(self.pointsNumber)]
        self.H = [deepcopy(templateMatrix) for _ in range(self.pointsNumber)]
        self.HTotal = deepcopy(templateMatrix)

        for point in range(self.pointsNumber):
            for i in range(nodeSize):
                for j in range(nodeSize):
                    self.dxH[point][i][j] = self.dx[point][i] * self.dx[point][j]
                    self.dyH[point][i][j] = self.dy[point][i] * self.dy[point][j]
                    self.H[point][i][j] = conductivity * self.jacobianDeterminants[point] * (self.dxH[point][i][j] + self.dyH[point][i][j])
                    self.HTotal[i][j] += self.H[point][i][j] * weights[point]

        # print('-----------------------------')
        # print(np.matrix(self.dxH[0]))
        # print()
        # print(np.matrix(self.dyH[0]))
        # print()
        # print(np.matrix(self.H[0]))
        # print()

    def printHTotal(self):
        print(np.matrix(self.HTotal))
        print()