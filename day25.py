from io import StringIO
from collections import deque


class Star:
    def __init__(self, pos, constellation=None):
        self.pos = pos
        self.constellation = constellation
        self.siblings = set()

    def __str__(self):
        return f"{self.pos} in {self.constellation} {self.siblings}"

    def __repr__(self):
        return f"Star({self.pos}, {self.constellation})"

    def __hash__(self):
        return hash(self.pos)


def load_file(f):
    res = []
    for line in f.readlines():
        res.append(Star(tuple(map(int, line.split(',')))))

    return res


def mdist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) + abs(a[3] - b[3])


def find_costellations(points):
    cid = 0

    for pa in points:
        for pb in points:
            if pa is not pb and mdist(pa.pos, pb.pos) <= 3:
                pa.siblings.add(pb)
                pb.siblings.add(pa)

    ungrouped = set(points)

    while ungrouped:
        curr = ungrouped.pop()
        cid += 1
        curr.constellation = cid

        todig = set(curr.siblings)
        while todig:
            child = todig.pop()
            if child not in ungrouped:
                continue

            child.constellation = curr.constellation
            ungrouped.remove(child)

            for sibling in child.siblings:
                if sibling in ungrouped:
                    todig.add(sibling)

    return cid


t1 = """0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0"""


t2 = """-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0"""


t3 = """1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2"""

#f = StringIO(t3)
f = open("day25.txt")
points = load_file(f)
print(find_costellations(points))
