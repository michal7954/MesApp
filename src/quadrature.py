from math import sqrt, pow

twoPoints = [
    [-1 / sqrt(3), 1 / sqrt(3)],
    [1, 1]
]

threePoints = [
    [-sqrt(3 / 5), 0, sqrt(3 / 5)],
    [5 / 9, 8 / 9, 5 / 9]
]


def f1(x):
    return -5 * pow(x, 2) + 2 * x - 8


def f2(ksi, eta):
    return 3 * pow(ksi, 2) * eta + 2 * ksi * pow(eta, 2) + 2


def quadrature(f, pointsNumber, dimension):
    if pointsNumber == 2:
        [P, W] = twoPoints
    elif pointsNumber == 3:
        [P, W] = threePoints
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


print(quadrature(f1, 2, 1))
print(quadrature(f1, 3, 1))

print(quadrature(f2, 2, 2))
print(quadrature(f2, 3, 2))
