import numpy as np
import sys

rackSize = 300


def powerlevel(x, y, serial):
    rackId = x+10
    pwrLvl = rackId * y
    pwrLvl += serial
    pwrLvl *= rackId
    return ((pwrLvl//100) % 10) - 5


def solve1(gridSerial):
    maxGridValue = - sys.maxsize - 1
    maxGridLocation = None
    subGridSize = 3

    for xg in range(rackSize-subGridSize+1):
        for yg in range(rackSize-subGridSize+1):

            subGridValue = 0
            for xs in range(xg, xg+subGridSize):
                for ys in range(yg, yg+subGridSize):
                    subGridValue += powerlevel(xs+1, ys+1, gridSerial)

            if subGridValue > maxGridValue:
                maxGridValue = subGridValue
                maxGridLocation = (xg+1, yg+1)

    return (maxGridValue, maxGridLocation)


def solve2(gridSerial):
    maxGridValue = - sys.maxsize - 1
    maxGridLocation = None

    sumtable = np.zeros((rackSize+1, rackSize+1), dtype=int)

    # create https://en.wikipedia.org/wiki/Summed-area_table
    # for fast area sum calculations
    for xg in range(1, rackSize):
        for yg in range(1, rackSize):
            currval = powerlevel(xg, yg, gridSerial)
            sumtable[xg, yg] = currval + sumtable[xg-1, yg] + \
                sumtable[xg, yg-1] - sumtable[xg-1, yg-1]

    for subGridSize in range(rackSize):
        for xg in range(rackSize-subGridSize):
            for yg in range(rackSize-subGridSize):

                subGridValue = sumtable[xg, yg] + \
                    sumtable[xg+subGridSize, yg+subGridSize] - \
                    sumtable[xg, yg+subGridSize] - \
                    sumtable[xg+subGridSize, yg]

                if subGridValue > maxGridValue:
                    maxGridValue = subGridValue
                    maxGridLocation = (xg+1, yg+1, subGridSize)

    return (maxGridValue, maxGridLocation)


maxGridValue, maxGridLocation = solve1(5235)
print("Solution 1", maxGridValue, " @", maxGridLocation)

maxGridValue, maxGridLocation = solve2(5235)
print("Solution 2", maxGridValue, " @", maxGridLocation)
