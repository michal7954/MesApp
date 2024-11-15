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
