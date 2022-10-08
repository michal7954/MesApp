class Element:
    id = None
    nodes = [None] * 4

    def __init__(self, dataString) -> None:
        stringParts = dataString.split(', ')
        self.id = int(stringParts[0])
        nodes = stringParts[1:]
        for i in range(len(nodes)):
            nodes[i] = int(nodes[i])
        self.nodes = nodes

    def __str__(self) -> str:
        stringNodesList = []
        for node in self.nodes:
            stringNodesList.append(node.id)
        return f'{self.id} -> {stringNodesList}'