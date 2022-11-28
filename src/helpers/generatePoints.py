from params.consts import quadraturePoints
from params.configuration import pointsScheme
from params.consts import nodeSize


def generatePoints():
    coords = quadraturePoints[pointsScheme]["coords"]
    weights = quadraturePoints[pointsScheme]["weights"]

    pointsList = []
    weightsList = []

    for i in range(pointsScheme):
        for j in range(pointsScheme):
            pointsList.append((coords[j], coords[i]))
            weightsList.append(weights[j] * weights[i])

    return [pointsList, weightsList]


[coords, weights] = generatePoints()


def generateBoundaryPoints():
    coords = quadraturePoints[pointsScheme]["coords"]
    weights = quadraturePoints[pointsScheme]["weights"]

    pointsList = [[] for _ in range(nodeSize)]
    weightsList = [[] for _ in range(nodeSize)]

    # dolny bok
    for i in range(pointsScheme):
        pointsList[0].append((coords[i], -1))
        weightsList[0].append(weights[i])

    # prawy bok
    for i in range(pointsScheme):
        pointsList[1].append((1, coords[i]))
        weightsList[1].append(weights[i])

    # górny bok
    for i in range(pointsScheme):
        pointsList[2].append((coords[i], 1))
        weightsList[2].append(weights[i])

    # lewy  bok
    for i in range(pointsScheme):
        pointsList[3].append((-1, coords[i]))
        weightsList[3].append(weights[i])

    # for row in pointsList:
    #     print(row)

    # for row in weightsList:
    #     print(row)

    return [pointsList, weightsList]


[boundaryCoords, boundaryWeights] = generateBoundaryPoints()
