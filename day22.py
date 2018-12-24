import numpy as np
import networkx as nx
from PIL import Image, ImageDraw


def scan(depth, target, extend=0):
    erosion = np.zeros(
        (target[0]+1+extend, target[1]+1+extend), dtype=np.int64)

    for x in range(target[0]+1+extend):
        for y in range(target[1]+1+extend):
            if (x == 0 and y == 0) or (x == target[0] and y == target[1]):
                erosion[x, y] = (0 + depth) % 20183
            elif x == 0:
                erosion[x, y] = ((y * 48271) + depth) % 20183
            elif y == 0:
                erosion[x, y] = ((x * 16807) + depth) % 20183
            else:
                erosion[x, y] = (
                    (erosion[x-1, y] * erosion[x, y-1]) + depth) % 20183

    return (lambda x: x % 3)(erosion)


depth = 510
target = (10, 10, 1)

# go real
if True:
    depth = 11991
    target = (6, 797, 1)

erosion = scan(depth, target)

print(erosion)
print("Solution1", np.sum(erosion))

# networx solution
erosion = scan(depth, target, 100)
gr = nx.MultiGraph()

# 0 neither, 1 torch, 2 climbing gear
tools = [set([1, 2]), set([0, 2]), set([0, 1])]

# sum = 0
for y in range(erosion.shape[1]):
    for x in range(erosion.shape[0]):
        for diff in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            xi, yi = x+diff[0], y+diff[1]
            if xi >= 0 and yi >= 0 and xi < erosion.shape[0] and yi < erosion.shape[1]:
                ma, mb = erosion[x, y], erosion[xi, yi]
                mat, mbt = tools[ma], tools[mb]

                same_tool = mat.intersection(mbt)
                for t in mat:
                    for s in mat.intersection(mbt):
                        gr.add_edge((x, y, t), (xi, yi, s),
                                    weight=8 if t != s else 1)

print("created graph")

# use
shortest = nx.dijkstra_path(gr, (0, 0, 1), target)
p = list(map(lambda e: gr[e[0]][e[1]][0]["weight"],
             (zip(shortest[:-1], shortest[1:]))))

s2 = list(map(lambda x: x[:2], shortest))

# print(shortest)
print(p, sum(p))
print(s2)

print("Solution 2", sum(p))

cell_size = 5
w, h = erosion.shape
img = Image.new('RGBA', (w*cell_size, h*cell_size), (255, 255, 255, 255))
draw = ImageDraw.Draw(img)

for x in range(w):
    for y in range(h):
        color = (0, 0, 0, 255)

        pos = (x, y)
        if pos == target:
            color = (0, 0, 0, 255)
        elif pos == (0, 0):
            color = (0, 0, 0, 255)
        elif pos in s2:
            color = (255, 50, 50, 255)
        else:
            env = erosion[pos]
            color = [
                (100, 100, 100, 255),
                (100, 200, 100, 255),
                (100, 100, 200, 255)][env]

        xi, yi = x*cell_size, y*cell_size
        draw.rectangle([xi, yi, xi+cell_size, yi+cell_size],
                       color)

img.show()
