from configuration import pointsScheme
from consts import nodeSize, quadraturePoints, shapeFunctions
import numpy as np


def generateCoords():
    coords = quadraturePoints[pointsScheme]["coords"]
    pointsList = []
    for i in range(pointsScheme):
        for j in range(pointsScheme):
            pointsList.append((coords[j], coords[i]))

    return pointsList


class Elem4:
    dKsi = []
    dEta = []
    points = 0
    coords = []

    def __init__(self) -> None:
        dKsiFuncs = shapeFunctions["dKsi"]
        dEtaFuncs = shapeFunctions["dEta"]
        self.points = pointsScheme**2
        self.coords = generateCoords()

        self.dKsi = [
            [dKsiFuncs[i](self.coords[j][1]) for i in range(nodeSize)]
            for j in range(pointsScheme**2)
        ]
        self.dEta = [
            [dEtaFuncs[i](self.coords[j][0]) for i in range(nodeSize)]
            for j in range(pointsScheme**2)
        ]

    def printKsiArray(self):
        dKsiOutput = [None for _ in range(self.points)]
        for i in range(self.points):
            dKsiOutput[i] = [self.coords[i][1]]
            dKsiOutput[i].extend(self.dKsi[i])
        print(np.matrix(dKsiOutput))

    def printEtaArray(self):
        dEtaOutput = [None for _ in range(self.points)]
        for i in range(self.points):
            dEtaOutput[i] = [self.coords[i][0]]
            dEtaOutput[i].extend(self.dEta[i])
        print(np.matrix(dEtaOutput))
