import re
from collections import deque
from PIL import Image, ImageDraw


def load_grid(filename):
    pattern = re.compile(r"(x|y)=(\d+), [x|y]=(\d+)..(\d+)")
    grid = dict()

    for line in open(filename).readlines():
        match = pattern.match(line)

        if match[1] == "x":
            x = int(match[2])
            for y in range(int(match[3]), int(match[4])+1):
                grid[(x, y)] = '#'
        else:
            y = int(match[2])
            for x in range(int(match[3]), int(match[4])+1):
                grid[(x, y)] = '#'

    return grid


def print_grid(clay, water):
    min_x = min(clay, key=lambda g: g[0])[0]
    max_x = max(clay, key=lambda g: g[0])[0]
    min_y = min(clay, key=lambda g: g[1])[1]
    max_y = max(clay, key=lambda g: g[1])[1]

    print(min_x, max_x, min_y, max_y)
    for y in range(min_y-1, max_y+2):
        line = ""
        for x in range(min_x-1, max_x+2):
            if (x, y) in clay:
                line += "\033[1;37;47m█\033[0m"
            elif (x, y) in water:
                w = water[x, y]
                if w == '~':
                    line += "\033[1;34;40m▓\033[0m"
                else:
                    line += "\033[1;34;40m░\033[0m"
            else:
                line += "."
        print(line)


def render_grid(clay, water):
    min_x = min(clay, key=lambda g: g[0])[0]
    max_x = max(clay, key=lambda g: g[0])[0]
    min_y = min(clay, key=lambda g: g[1])[1]
    max_y = max(clay, key=lambda g: g[1])[1]

    w, h = max_x - min_x, max_y - min_y
    img = Image.new('RGBA', (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            dp = (x-min_x, y-min_y)
            if (x, y) in clay:
                draw.point(dp, (20, 20, 10, 255))
            elif (x, y) in water:
                w = water[x, y]
                if w == '~':
                    draw.point(dp, (20, 20, 255, 255))
                else:
                    draw.point(dp, (200, 200, 255, 255))

    return img


# there is lot of optimization oportunities here
# flows could be refactored to one function with direction parameter
# using dicts for points should be changed to arrays
def start_flow(clay, water, x, y):
    max_y = max(clay, key=lambda g: g[1])[1]

    pos = (x, y)
    while True:
        water[pos] = "|"
        nextpos = (pos[0], pos[1]+1)

        if nextpos[1] > max_y:
            return []
        if nextpos in water and water[nextpos] == "|":
            return []

        if nextpos in clay or nextpos in water and water[nextpos] == "~":
            break

        pos = nextpos

    touchpoint = pos

    # flow left
    left_edge = None
    left_drip = None
    while True:
        water[pos] = "|"
        posleft = (pos[0]-1, pos[1])
        posdown = (pos[0], pos[1]+1)

        if not(posdown in clay or posdown in water and water[posdown] == "~"):
            left_drip = pos
            break

        if posleft in clay:
            left_edge = pos
            break
        pos = posleft

    pos = touchpoint

    # flow right
    right_edge = None
    right_drip = None
    while True:
        water[pos] = "|"
        posright = (pos[0]+1, pos[1])
        posdown = (pos[0], pos[1]+1)

        if not (posdown in clay or posdown in water and water[posdown] == "~"):
            right_drip = pos
            break

        if posright in clay:
            right_edge = pos
            break

        pos = posright

    if left_edge and right_edge:
        for x in range(left_edge[0], right_edge[0]+1):
            water[x, left_edge[1]] = "~"
        return [(touchpoint[0], touchpoint[1]-1)]

    return [left_drip, right_drip]


clay = load_grid("day17.txt")
water = dict()

dripstarts = deque()
dripstarts.append((500, 0))

while dripstarts:
    curflow = dripstarts.popleft()
    if curflow:
        overlows = start_flow(clay, water, *curflow)
        dripstarts.extend(overlows)


min_y = min(clay, key=lambda g: g[1])[1]
print("solution 1:", len(list(filter(lambda w: w[1] >= min_y, water))))
print("solution 2:", len(
    list(filter(lambda key: key[1] >= min_y and water[key] == "~", water))))


image = render_grid(clay, water)
image.show()
image.close()
