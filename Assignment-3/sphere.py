from math import sin, cos, pi

import numpy as np


def parametricSurface(uStart, uEnd, uResolution, vStart, vEnd, vResolution, surfaceFunction):
    deltaU = (uEnd - uStart) / uResolution
    deltaV = (vEnd - vStart) / vResolution
    positions = []

    for uIndex in range(uResolution + 1):
        vArray = []
        for vIndex in range(vResolution + 1):
            u = uStart + uIndex * deltaU
            v = vStart + vIndex * deltaV
            vArray.append(surfaceFunction(u, v))
        positions.append(vArray)

    positionData = []
    for xIndex in range(uResolution):
        for yIndex in range(vResolution):
            pA = positions[xIndex][yIndex]
            pB = positions[xIndex + 1][yIndex]
            pD = positions[xIndex][yIndex + 1]
            pC = positions[xIndex + 1][yIndex + 1]
            positionData += [pA, pB, pC, pA, pC, pD]
    return positionData

def generateSphere(radiusSegments=32, heightSegments=16):
    radius = 1.0

    def S(u, v):
        x = radius * sin(u) * cos(v)
        y = radius * sin(v)
        z = radius * cos(u) * cos(v)
        return [x, y, z, x, y, z]  # Position and Normal are the same for a unit sphere

    positions = parametricSurface(0, 2 * pi, radiusSegments, -pi / 2, pi / 2, heightSegments, S)
    return np.array(positions, dtype=np.float32).reshape(-1)