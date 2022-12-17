from classes.Node import Node
from classes.Element import Element
from classes.Grid import Grid
from classes.GlobalData import GlobalData
from params.configuration import inputFileIndex
from params.consts import inputFileLocationList

inputFile = open(inputFileLocationList[inputFileIndex], "r")
fileParts = inputFile.read().split("\n*")
for i in range(len(fileParts)):
    fileParts[i] = fileParts[i].split("\n")

globalData = None


def initGlobalData():
    global globalData
    params = fileParts[0]
    globalData = GlobalData(params)
    return globalData


def initGrid():
    nodes = fileParts[1][1:]
    elements = fileParts[2][1:]
    boundaryConditions = fileParts[3][1]

    nodesList = []
    for nodeData in nodes:
        nodesList.append(Node(nodeData, globalData.initialTemp))

    # uwzględnienie warunków brzegowych
    boundaryNodesList = [int(id) for id in boundaryConditions.split(", ")]
    for i in range(len(nodesList)):
        if nodesList[i].id in boundaryNodesList:
            nodesList[i].boundaryCondition = 1

    elementsList = []
    for elementData in elements:
        elementsList.append(Element(elementData))

    # podmiana indeksów wierzchołków na odpowiednie wzkaźniki do obiektów Node
    for i in range(len(elementsList)):
        nodes = elementsList[i].nodes
        for j in range(len(nodes)):
            nodeId = nodes[j]
            nodeObject = nodesList[nodeId - 1]
            elementsList[i].nodes[j] = nodeObject

    grid = Grid(nodesList, elementsList, globalData.initialTemp)

    return grid
