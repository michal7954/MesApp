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
        # print(f'Nodes number: {self.nodesNumber}')
        # print(f'Elements number: {self.elementsNumber}')
        print()

    def __str__(self) -> str:
        return str(self.simulationTime)
