from modules.initData import initGlobalData, initGrid
from classes.Elem4 import elem4
from helpers.generatePoints import coords
from numpy import matrix


def main():
    globalData = initGlobalData()
    grid = initGrid()

    # globalData.print()
    # grid.print()

    # print('Wygenerowane punkty całkowania [ksi, eta]')
    # print(matrix(coords))
    # print()

    # elem4.printKsiArray()
    # elem4.printEtaArray()

    # obliczenia związane z całką H na każdym elemencie
    for element in grid.elements:
        # element.printHeader()

        element.calculateJacobians()
        # element.printJacobians()

        element.calculateShapeFunctionsDerivates()
        # element.printShapeFuncitonsDerivates()

        element.calculateH(globalData.conductivity)
        # element.printHTotal()

        element.countBoundaryConditionH(globalData.alfa)
        # element.printBoundaryConditionH()

        element.calculateP(globalData.alfa, globalData.tot)
        # element.printP()

        element.calculateC(globalData.specificHeat, globalData.density)
        # element.printC()

    grid.calculateHG()
    grid.printHG()

    grid.calculatePG()
    grid.printPG()

    grid.calculateCG()
    grid.printCG()

    grid.simulate(globalData.simulationStepTime)
    grid.printSolution()


if __name__ == "__main__":
    main()
