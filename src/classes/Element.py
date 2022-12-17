import numpy as np
from copy import deepcopy
from classes.Elem4 import elem4
from params.configuration import pointsScheme
from params.consts import elementSize
from helpers.generatePoints import weights, boundaryWeights
from helpers.distance import distance
from helpers.printTable import printTable


class Element:
    id = None
    nodes = [None] * elementSize
    pointsNumber = pointsScheme**2

    jacobianMatrices = []
    jacobianDeterminants = []
    invertibleJacobianMatrices = []

    dx = []
    dy = []

    dxH = []
    dyH = []
    HPartial = []
    HTotal = []

    boundaryConditionH = []

    P = []

    C = []

    def __init__(self, dataString) -> None:
        stringParts = dataString.split(", ")
        self.id = int(stringParts[0])
        nodes = stringParts[1:]
        for i in range(len(nodes)):
            nodes[i] = int(nodes[i])
        self.nodes = nodes

    def __str__(self) -> str:
        stringNodesList = []
        for node in self.nodes:
            stringNodesList.append(node.id)
        return f"{self.id} -> {stringNodesList}"

    def printHeader(self):
        print("-----------------------------------")
        print("Element", self.id)

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
            for i in range(elementSize):
                globalCoords.append(self.nodes[i].x)
        elif globalCoordsType == 1:
            for i in range(elementSize):
                globalCoords.append(self.nodes[i].y)

        # wybranie wartości pochodnych po odpowiedniej współrzędnej lokalnej i dla odpowiedniego punktu całkowania
        if localCoordsType == 0:
            valuesList = elem4.dKsi[point]
        elif localCoordsType == 1:
            valuesList = elem4.dEta[point]

        # interpolacja elementu macierzy Jacobiego
        sum = 0
        for i in range(elementSize):
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

        print("Macierze Jakobiego")
        print(np.matrix(outputJacobianTable))
        print()
        print("Jakobiany")
        print(np.array(self.jacobianDeterminants))
        print()
        print("Odwrotne macierze Jakobiego (po podzieleniu przez wyznacznik)")
        print(np.matrix(outputInvertibleJacobianTable))
        print()

    def calculateShapeFunctionsDerivates(self):
        self.dx = [[0 for _ in range(elementSize)] for _ in range(self.pointsNumber)]
        self.dy = [[0 for _ in range(elementSize)] for _ in range(self.pointsNumber)]

        for point in range(self.pointsNumber):
            for i in range(elementSize):
                self.dx[point][i] = self.invertibleJacobianMatrices[point][0][0] * elem4.dKsi[point][i] + self.invertibleJacobianMatrices[point][0][1] * elem4.dEta[point][i]
                self.dy[point][i] = self.invertibleJacobianMatrices[point][1][0] * elem4.dKsi[point][i] + self.invertibleJacobianMatrices[point][1][1] * elem4.dEta[point][i] 

    def printShapeFuncitonsDerivates(self):
        print("dN_i/dx")
        print(np.matrix(self.dx))
        print()
        print("dN_i/dy")
        print(np.matrix(self.dy))
        print()

    def calculateH(self, conductivity):
        templateMatrix = [[0 for _ in range(elementSize)] for _ in range(elementSize)]

        self.dxH = [deepcopy(templateMatrix) for _ in range(self.pointsNumber)]
        self.dyH = [deepcopy(templateMatrix) for _ in range(self.pointsNumber)]
        self.HPartial = [deepcopy(templateMatrix) for _ in range(self.pointsNumber)]
        self.HTotal = deepcopy(templateMatrix)

        for point in range(self.pointsNumber):
            for i in range(elementSize):
                for j in range(elementSize):
                    self.dxH[point][i][j] = self.dx[point][i] * self.dx[point][j]
                    self.dyH[point][i][j] = self.dy[point][i] * self.dy[point][j]
                    self.HPartial[point][i][j] = conductivity * self.jacobianDeterminants[point] * (self.dxH[point][i][j] + self.dyH[point][i][j])
                    self.HTotal[i][j] += self.HPartial[point][i][j] * weights[point]

    def printHTotal(self):
        print("Macierz H (po zsumowaniu)")
        print(np.matrix(self.HTotal))
        print()

    def countBoundaryConditionH(self, alfa):
        self.boundaryConditionH = [[0 for _ in range(elementSize)] for _ in range(elementSize)]
        
        for side in range(elementSize):
            nodeA = side
            nodeB = (side + 1) % elementSize

            # jeśli bok nie należy do brzegu nie uwzględniaj go w macierzy boundaryConditionH
            if not (self.nodes[nodeA].boundaryCondition and self.nodes[nodeB].boundaryCondition):
                continue

            detJ = distance(self.nodes[nodeA], self.nodes[nodeB]) / 2
            # print(detJ)

            for point in range(pointsScheme):
                for i in range(elementSize):
                    for j in range(elementSize):
                        # bezpośrednio na podstawie wzoru całkowania
                        # z pominięciem pośrednich macierzy dla poszczególnych punktów całkowania
                        # z pominięciem jawnej macierzy {N}{N}^T
                        self.boundaryConditionH[i][j] += (
                            boundaryWeights[side][point]
                            * alfa
                            * elem4.boundaryPointsN[side][point][i]
                            * elem4.boundaryPointsN[side][point][j]
                            * detJ
                        )

        # dodanie warunku brzegowego do ostatecznej macierzy H elementu
        for i in range(elementSize):
            for j in range(elementSize):
                self.HTotal[i][j] += self.boundaryConditionH[i][j]

    def printBoundaryConditionH(self):
        printTable(self.boundaryConditionH, 8, 4)
        print()

    def calculateP(self, alfa, tot):
        self.P = [0 for _ in range(elementSize)]

        for side in range(elementSize):
            nodeA = side
            nodeB = (side + 1) % elementSize

            # jeśli bok nie należy do brzegu nie uwzględniaj go w macierzy P
            if not (self.nodes[nodeA].boundaryCondition and self.nodes[nodeB].boundaryCondition):
                continue

            detJ = distance(self.nodes[nodeA], self.nodes[nodeB]) / 2

            for point in range(pointsScheme):
                for i in range(elementSize):
                    # bezpośrednio na podstawie wzoru całkowania
                    # z pominięciem pośrednich macierzy dla poszczególnych punktów całkowania
                    self.P[i] += (
                        alfa
                        * boundaryWeights[side][point]
                        * elem4.boundaryPointsN[side][point][i]
                        * tot
                        * detJ
                    )

    def printP(self):
        print(self.P)
        print()

    def calculateC(self, specificHeat, density):
        self.C = [[0 for _ in range(elementSize)] for _ in range(elementSize)]

        for point in range(self.pointsNumber):
            for i in range(elementSize):
                for j in range(elementSize):
                    self.C[i][j] += (
                        specificHeat
                        * density
                        * elem4.NxNT[point][i][j]
                        * weights[point]
                        * self.jacobianDeterminants[point]
                    )

    def printC(self):
        printTable(self.C, 8, 2)
        print()
