import numpy as np
import matplotlib.pyplot as plt


# Step function u(0.0)
def Step(t, V):
    if t <= 0.0:
        return 0
    else:
        return V


def CalcRLCGraph(RLCV):
    # params
    R = RLCV[0]  # ohms
    L = RLCV[1]  # henrys
    C = RLCV[2]  # farads
    V = RLCV[3]  # volt

    # Time settings
    tStart = 0
    tEnd = RLCV[4]  # seconds
    tDist = RLCV[5]  # seconds
    numPoints = int((tEnd - tStart) / tDist)  # number of plotting points
    print("num_points", numPoints)

    # Included Q in C
    qBef = 0
    qNow = 0
    timeSeries = []
    currentSeries = []
    vXSeries = [[], [], []]
    for t in np.linspace(tStart, tEnd, numPoints):
        vC = qNow / C
        qDistNow = (qNow - qBef) / tDist
        vR = R * qDistNow
        # vL=L*(qDistNow-qDistBef)/tDist
        vL = Step(t, V) - vR - vC
        # vL=LI''=(qNext+qBef-2qNow)*(L/t^2)
        qNext = vL / (L / (tDist * tDist)) - qBef + 2 * qNow
        timeSeries.append(t)
        currentSeries.append(qDistNow)
        vXSeries[0].append(vR)
        vXSeries[1].append(vL)
        vXSeries[2].append(vC)

        qBef = qNow
        qNow = qNext

    # Create the time-voltage graph
    return [timeSeries, currentSeries, vXSeries]
