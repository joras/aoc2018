import numpy as np


def load_grid(filename, w=50, h=50):
    grid = np.zeros((w+2, h+2), dtype=np.character)
    for x, line in enumerate(open(filename).readlines()):
        for y, char in enumerate(line.strip('\n')):
            grid[x+1, y+1] = char

    return grid


def magic(grid):
    newgrid = grid.copy()

    for x in range(1, grid.shape[0]-1):
        for y in range(1, grid.shape[1]-1):
            acre = grid[x, y]

            counts = {b'#': 0, b'|': 0, b'.': 0, b'': 0}
            for xi in range(-1, 2):
                for yi in range(-1, 2):
                    if not (xi == 0 and yi == 0):
                        counts[forest[x+xi, y+yi]] += 1
            if acre == b'.' and counts[b'|'] >= 3:
                newgrid[x, y] = b'|'
                pass
            elif acre == b'|' and counts[b'#'] >= 3:
                newgrid[x, y] = b'#'
            elif acre == b'#' and not (counts[b'#'] > 0 and counts[b'|'] > 0):
                newgrid[x, y] = b'.'

    return newgrid


def print_forest(forest):
    for line in forest:
        print("".join(map(lambda c: c.decode('UTF-8'), line)))


forest = load_grid("day18.txt", 50, 50)
print_forest(forest)

hashes = {}
period = 0

i = 1
while True:
    forest = magic(forest)
    print_forest(forest)

    if i == 10:
        stats = dict(zip(*np.unique(forest, return_counts=True)))
        print("Solution 1: ", stats[b'#']*stats[b'|'])
    elif i == 1000000000:
        stats = dict(zip(*np.unique(forest, return_counts=True)))
        print("Solution 2: ", stats[b'#']*stats[b'|'])
        break

    newhash = hash(forest.data.tobytes())
    if not period and newhash in hashes:
        goal = 1000000000
        remaining = goal - i

        period = i - hashes[newhash]
        remaining = (remaining // period) * period
        i += remaining + 1

    else:
        hashes[newhash] = i
        i += 1
