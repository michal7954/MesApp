from initData import initGlobalData, initGrid
from classes.Elem4 import Elem4

def main():
    # globalData = initGlobalData()
    # grid = initGrid()

    # globalData.print()
    # grid.print()
    
    elem4 = Elem4()

    print('--------------------------------')
    elem4.printKsiArray()
    print('--------------------------------')
    elem4.printEtaArray()

if __name__ == '__main__':
    main()
