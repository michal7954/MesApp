from math import sqrt

twoPointsQuadrature = [
    [-1 / sqrt(3), 1 / sqrt(3)],
    [1, 1]
]

threePointsQuadrature = [
    [-sqrt(3 / 5), 0, sqrt(3 / 5)],
    [5 / 9, 8 / 9, 5 / 9]
]

fourPointsQuadrature = [
    [
        -sqrt(3 / 7 + 2 / 7 * sqrt(6 / 5)),
        -sqrt(3 / 7 - 2 / 7 * sqrt(6 / 5)),
        sqrt(3 / 7 - 2 / 7 * sqrt(6 / 5)),
        sqrt(3 / 7 + 2 / 7 * sqrt(6 / 5)),
    ],
    [
        (18 - sqrt(30)) / 36,
        (18 + sqrt(30)) / 36,
        (18 + sqrt(30)) / 36,
        (18 - sqrt(30)) / 36,
    ],
]

quadraturePoints = {
    2: {
        "coords": twoPointsQuadrature[0],
        "weights": twoPointsQuadrature[1]
    },
    3: {
        "coords": threePointsQuadrature[0],
        "weights": threePointsQuadrature[1]
    },
    4: {
        "coords": fourPointsQuadrature[0],
        "weights": fourPointsQuadrature[1]
    },
}

nodeSize = 4

shapeFunctions = {
    "func": [
        lambda ksi, eta: (1 - ksi) * (1 - eta) / 4,
        lambda ksi, eta: (1 + ksi) * (1 - eta) / 4,
        lambda ksi, eta: (1 + ksi) * (1 + eta) / 4,
        lambda ksi, eta: (1 - ksi) * (1 + eta) / 4,
    ],
    "dKsi": [
        lambda eta: -(1 - eta) / 4,
        lambda eta: (1 - eta) / 4,
        lambda eta: (1 + eta) / 4,
        lambda eta: -(1 + eta) / 4,
    ],
    "dEta": [
        lambda ksi: -(1 - ksi) / 4,
        lambda ksi: -(1 + ksi) / 4,
        lambda ksi: (1 + ksi) / 4,
        lambda ksi: (1 - ksi) / 4,
    ],
}


# for fun in shapeFunctions:
#     print(fun(-1,-1))