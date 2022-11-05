from params.consts import quadraturePoints
from params.configuration import pointsScheme

def generateCoords():
    coords = quadraturePoints[pointsScheme]["coords"]
    pointsList = []
    for i in range(pointsScheme):
        for j in range(pointsScheme):
            pointsList.append((coords[j], coords[i]))

    return pointsList

coords = generateCoords()