import numpy as np
from params.configuration import pointsScheme
from params.consts import nodeSize, shapeFunctions
from helpers.generatePoints import coords, boundaryCoords


class Elem4:
    pointsNumber = pointsScheme**2

    coords = coords
    dKsi = []
    dEta = []

    boundaryCoords = boundaryCoords
    boundaryPointsN = []

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

        # obliczanie wartości funkcji kształtu dla punktów całkowania warunku brzegowego
        self.boundaryPointsN = [[[0 for _ in range(nodeSize)] for _ in range(pointsScheme)] for _ in range(nodeSize)]
        NFuncs = shapeFunctions["func"]

        # bok elementu skończonego
        for side in range(nodeSize):
            # kolejne punkty całkowania na boku
            for point in range(pointsScheme):
                # funkcje kształtu kolejnych węzłów
                for node in range(nodeSize):
                    # N_i(ksi, eta)
                    self.boundaryPointsN[side][point][node] = NFuncs[node](
                        boundaryCoords[side][point][0], boundaryCoords[side][point][1]
                    )

        # for side in self.boundaryPointsN:
        #     for point in side:
        #         print(point)

    def printKsiArray(self):
        print("dN_i/dKsi")
        print(np.matrix(self.dKsi))
        print()

    def printEtaArray(self):
        print("dN_i/dEta")
        print(np.matrix(self.dEta))
        print()


elem4 = Elem4()
