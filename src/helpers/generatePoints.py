from params.consts import quadraturePoints
from params.configuration import pointsScheme

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