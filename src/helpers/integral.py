from params.consts import twoPointsQuadrature, threePointsQuadrature


def integrate(f, dimension, pointsNumber=3, x_1=-1, x_2=1):
    if dimension not in [1]:
        return None

    if pointsNumber == 2:
        [P, W] = twoPointsQuadrature
    elif pointsNumber == 3:
        [P, W] = threePointsQuadrature
    else:
        return None

    # mapowanie punktów całkowania Gaussa z przedziału [-1, 1] na zadany przedział całkowania [x_1, x_2]
    PCX = []
    for point in P:
        PCX.append((1 - point) / 2 * x_1 + (1 + point) / 2 * x_2)

    # obliczenie wyznacznika macierzy Jacobiego
    detJ = (x_2 - x_1) / 2

    return weightSum(f, dimension, pointsNumber, PCX, W) * detJ


def weightSum(f, dimension, pointsNumber, P, W):
    sum = 0
    for i in range(pointsNumber):
        if dimension == 1:
            sum += f(P[i]) * W[i]
        # do obsługi dwóch wymarów potrzebne jest bardzej skomplikowane przekształcenie macierzowe


def f(x):
    return x**2 - 2 * x + 2


print(integrate(f, 1, 2, -2, 6))
print(integrate(f, 1, 3, -2, 6))

# def f1(x):
#     return -5 * pow(x, 2) + 2 * x - 8

# print(integrate(f1, 1))
