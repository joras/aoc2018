from dataclasses import dataclass
import re
import sys
import time

from PIL import Image, ImageDraw


@dataclass
class Star:
    x: int
    y: int
    xspeed: int
    yspeed: int


starmap = []
for line in open('day10.txt'):
    m = re.match(
        r"position=<([ -]+\d+), ([ -]+\d+)> velocity=<([ -]+\d+), ([ -]+\d+)>", line)
    starmap.append(Star(int(m[1]), int(m[2]), int(m[3]), int(m[4])))


acc = 100
prevCirc = sys.maxsize
step = 0
found = False

while True:
    for star in starmap:
        star.x += star.xspeed * acc
        star.y += star.yspeed * acc

    step += acc

    maxx = max(starmap, key=lambda x: x.x).x
    maxy = max(starmap, key=lambda x: x.y).y
    minx = min(starmap, key=lambda x: x.x).x
    miny = min(starmap, key=lambda x: x.y).y

    circ = (maxx - minx) + (maxy - miny)
    width = maxy - miny

    # slow down, now that we could render this image
    if (maxx < 500):
        acc = 1

    if found:
        print("Solution: ", step)
        # show the image
        img = Image.new('RGB', (maxx-minx+6, maxy-miny+6), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        for star in starmap:
            draw.point((star.x - minx+3, star.y-miny+3), (255, 0, 0))

        img.show()
        break

    # we're growing again, go back one step
    if prevCirc < circ:
        acc = -1
        found = True

    prevCirc = circ
