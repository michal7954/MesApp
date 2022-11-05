from math import pow
from params.consts import twoPointsQuadrature, threePointsQuadrature


def f1(x):
    return -5 * pow(x, 2) + 2 * x - 8


def f2(ksi, eta):
    return 3 * pow(ksi, 2) * eta + 2 * ksi * pow(eta, 2) + 2


def quadrature(f, dimension, pointsNumber=3):
    if pointsNumber == 2:
        [P, W] = twoPointsQuadrature
    elif pointsNumber == 3:
        [P, W] = threePointsQuadrature
    else:
        return None

    sum = 0
    for i in range(pointsNumber):
        if dimension == 1:
            sum += f(P[i]) * W[i]
        else:
            for j in range(pointsNumber):
                if dimension == 2:
                    sum += f(P[i], P[j]) * W[i] * W[j]
                else:
                    return None

    return sum


print(quadrature(f1, 1, 2))
print(quadrature(f1, 1, 3))

print(quadrature(f2, 2, 2))
print(quadrature(f2, 2, 3))
