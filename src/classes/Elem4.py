import numpy as np
from params.configuration import pointsScheme
from params.consts import nodeSize, shapeFunctions
from helpers.generatePoints import coords

class Elem4:
    dKsi = []
    dEta = []
    pointsNumber = pointsScheme**2
    coords = coords

    def __init__(self) -> None:
        # załadowanie listy pochodnych funkcji kształtu
        dKsiFuncs = shapeFunctions["dKsi"]
        dEtaFuncs = shapeFunctions["dEta"]

        # obliczenie wartości pochodnych po dwóch zmiennych funkcji kształtu w poszczególnych punktach całkowania
        # i-ta funkcja kształtu
        # j-ty punkt całkowania

        # dKsi - tablica zawierająca wartości pochodnych po ksi, których argumentem jest eta (druga współrzędna)
        self.dKsi = [
            [dKsiFuncs[i](self.coords[j][1]) for i in range(nodeSize)]
            for j in range(self.pointsNumber)
        ]
        # dEta - tablica zawierająca wartości pochodnych po eta, których argumentem jest ksi (pierwsza współrzędna)
        self.dEta = [
            [dEtaFuncs[i](self.coords[j][0]) for i in range(nodeSize)]
            for j in range(self.pointsNumber)
        ]

    def printKsiArray(self):
        dKsiOutput = [None for _ in range(self.pointsNumber)]
        for i in range(self.pointsNumber):
            dKsiOutput[i] = [self.coords[i][1]]
            dKsiOutput[i].extend(self.dKsi[i])

        print('---------------------------------------------------------------')
        print(np.matrix(dKsiOutput))
        print()

    def printEtaArray(self):
        dEtaOutput = [None for _ in range(self.pointsNumber)]
        for i in range(self.pointsNumber):
            dEtaOutput[i] = [self.coords[i][0]]
            dEtaOutput[i].extend(self.dEta[i])

        print('---------------------------------------------------------------')
        print(np.matrix(dEtaOutput))
        print()

elem4 = Elem4()