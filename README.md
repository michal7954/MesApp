# Finite Element Method

This project is an Object-Oriented Programming (OOP) software tool designed to perform simulations using the Finite Element Method (FEM). The software is implemented in Python and aims to provide a flexible and extensible framework for FEM simulations, allowing users to model and analyze physical phenomena such as heat transfer, structural analysis, and more.

## Key Use Cases

1. **Heat Transfer Simulation**:
   - MesApp can be used to simulate heat distribution and transfer within a given material or structure.
   - It allows the definition of initial and boundary conditions and computes the temperature distribution over time.

2. **Structural Analysis**:
   - The software enables the simulation of stress and strain within structures under various load conditions.
   - Users can define material properties, boundary constraints, and load applications.

## Code Highlights

### Node Class

The [Node.py](https://github.com/michal7954/MesApp/blob/main/src/classes/Node.py) file declares a class that represents a node in the FEM mesh, storing its coordinates, temperature, and boundary conditions.

```python
class Node:
    id = None
    x = None
    y = None
    temperature = None
    boundaryCondition = None

    def __init__(self, dataString, initialTemp) -> None:
        stringParts = dataString.split(", ")

        self.id = int(stringParts[0].strip())
        self.x = float(stringParts[1].strip())
        self.y = float(stringParts[2].strip())

        self.temperature = initialTemp
        self.boundaryCondition = 0

    def __str__(self) -> str:
        return f"{self.id} -> ({self.x}, {self.y}) -> {self.boundaryCondition}"
```

### Global Data Initialization

The [initData.py](https://github.com/michal7954/MesApp/blob/main/src/modules/initData.py) module initializes global simulation parameters and the FEM grid based on input file.

```python
from classes.Node import Node
from classes.Element import Element
from classes.Grid import Grid
from classes.GlobalData import GlobalData
from params.configuration import inputFileIndex
from params.consts import inputFilesDirectory, inputFileLocationList

inputFile = open(f'{inputFilesDirectory}{inputFileLocationList[inputFileIndex]}', "r")
fileParts = inputFile.read().split("\n*")
for i in range(len(fileParts)):
    fileParts[i] = fileParts[i].split("\n")

globalData = None

def initGlobalData() -> GlobalData:
    global globalData
    params = fileParts[0]
    globalData = GlobalData(params)
    return globalData

def initGrid() -> Grid:
    nodes = fileParts[1][1:]
    elements = fileParts[2][1:]
    boundaryConditions = fileParts[3][1]

    nodesList = []
    for nodeData in nodes:
        nodesList.append(Node(nodeData, globalData.initialTemp))

    boundaryNodesList = [int(id) for id in boundaryConditions.split(", ")]
    for i in range(len(nodesList)):
        if nodesList[i].id in boundaryNodesList:
            nodesList[i].boundaryCondition = 1

    elementsList = []
    for elementData in elements:
        elementsList.append(Element(elementData))

    for i in range(len(elementsList)):
        nodes = elementsList[i].nodes
        for j in range(len(nodes)):
            nodeId = nodes[j]
            nodeObject = nodesList[nodeId - 1]
            elementsList[i].nodes[j] = nodeObject

    grid = Grid(nodesList, elementsList, globalData.initialTemp)

    return grid
```

### GlobalData Class

The [GlobalData.py](https://github.com/michal7954/MesApp/blob/main/src/classes/GlobalData.py) stores global parameters for the FEM simulation.

```python
class GlobalData:
    simulationTime = None
    simulationStepTime = None
    conductivity = None
    alfa = None
    tot = None
    initialTemp = None
    density = None
    specificHeat = None
    nodesNumber = None
    elementsNumber = None

    def __init__(self, params) -> None:
        parametersDict = {}

        for param in params:
            splitIdx = param.rfind(" ")
            key = param[:splitIdx].strip()
            value = param[splitIdx:].strip()
            parametersDict[key] = int(value)

        self.simulationTime = parametersDict["SimulationTime"]
        self.simulationStepTime = parametersDict["SimulationStepTime"]
        self.conductivity = parametersDict["Conductivity"]
        self.alfa = parametersDict["Alfa"]
        self.tot = parametersDict["Tot"]
        self.initialTemp = parametersDict["InitialTemp"]
        self.density = parametersDict["Density"]
        self.specificHeat = parametersDict["SpecificHeat"]
        self.nodesNumber = parametersDict["Nodes number"]
        self.elementsNumber = parametersDict["Elements number"]

    def print(self):
        print(f"SimulationTime: {self.simulationTime}")
        print(f"SimulationStepTime: {self.simulationStepTime}")
        print(f"Conductivity: {self.conductivity}")
        print(f"Alfa: {self.alfa}")
        print(f"Tot: {self.tot}")
        print(f"InitialTemp: {self.initialTemp}")
        print(f"Density: {self.density}")
        print(f"SpecificHeat: {self.specificHeat}")
        print()

    def __str__(self) -> str:
        return str(self.simulationTime)
```
