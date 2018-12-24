import re


def load_file(filename):
    bots = []
    digit = re.compile(r"-?\d+")
    for line in open(filename).readlines():
        b = tuple(map(int, digit.findall(line)))
        bots.append(b)
    return bots


def mdist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])+abs(a[2] - b[2])


def n_bots_range(pos, bots):
    count = 0
    for b in bots:
        if abs(pos[0] - b[0]) + abs(pos[1] - b[1])+abs(pos[2] - b[2]) <= b[3]:
            count += 1

    return count


bots = load_file("day23.txt")
strongest = max(bots, key=lambda b: b[3])
inrange = list(filter(lambda b: mdist(b, strongest) <= strongest[3], bots))
print("Solution 1:", len(inrange))

x_min = min(bots, key=lambda b: b[0] - b[3])
x_min = x_min[0] - x_min[3]

x_max = max(bots, key=lambda b: b[0]+b[3])
x_max = x_max[0] + x_max[3]

stepdiv = 2
step = (x_max-x_min)
cpoint = (0, 0, 0)

points = []

# I have a feeling that it is not quite general solution
# needs revisiting at some point
while True:
    points = []

    for x in range(-stepdiv, stepdiv+1):
        for y in range(-stepdiv, stepdiv+1):
            for z in range(-stepdiv, stepdiv+1):
                pdiff = (x*step, y*step, z*step)
                spoint = (cpoint[0]+pdiff[0], cpoint[1] +
                          pdiff[1], cpoint[1]+pdiff[1])
                points.append((spoint, n_bots_range(spoint, bots)))

    cpoint = max(points, key=lambda p: p[1])[0]
    if step == 1:
        break

    step = step//stepdiv
    if step == 0:
        step = 1

mpoint = max(points, key=lambda p: p[1])
print("Solution 2:", mdist((0, 0, 0), mpoint[0]))
