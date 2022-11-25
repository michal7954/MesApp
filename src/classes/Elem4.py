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
        print("dN_i/dKsi")
        print(np.matrix(self.dKsi))
        print()

    def printEtaArray(self):
        print("dN_i/dEta")
        print(np.matrix(self.dEta))
        print()


elem4 = Elem4()
