from modules.initData import initGlobalData, initGrid
from classes.Elem4 import elem4

def main():
    globalData = initGlobalData()
    grid = initGrid()

    # globalData.print()
    # grid.print()

    # elem4.printKsiArray()
    # elem4.printEtaArray()

    # for element in grid.elements:
    #     element.printJacobians()
    #     element.printShapeFuncitonsDerivates()
    #     element.printHTotal()

if __name__ == '__main__':
    main()
