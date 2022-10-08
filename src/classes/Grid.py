class Grid:
    nodesNumber = None
    elementsNumber = None
    nodes = []
    elements = []

    def print(self):
        print(f'Nodes number: {self.nodesNumber}')

        print('Nodes:')
        for node in self.nodes:
            print(node)
        
        print()
        print(f'Elements number: {self.elementsNumber}')
        print('Elements:')
        for element in self.elements:
            print(element)