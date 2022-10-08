from initData import initGlobalData, initGrid

def main():
    globalData = initGlobalData()
    grid = initGrid()

    globalData.print()
    grid.print()

if __name__ == '__main__':
    main()
