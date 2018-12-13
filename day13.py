from dataclasses import dataclass
from functools import reduce


@dataclass
class Cart:
    direction: str
    x: int
    y: int
    nextTurn: str
    crashed: bool


def loadFile(filename):
    grid = []
    carts = []

    for y, line in enumerate(open(filename).readlines()):
        # for char in line:
        curLine = []
        for x, char in enumerate(line.strip('\n')):
            cartChar = "<>v^"
            if char in cartChar:
                carts.append(Cart(char, x, y, 0, False))
                curLine.append("--||"[cartChar.find(cartChar)])
            else:
                curLine.append(char)

        grid.append(curLine)

    return grid, carts


def printNetwork(grid, carts):
    cartsDict = {(cart.x, cart.y): cart for cart in carts}

    for y, line in enumerate(grid):
        pLine = []
        for x, char in enumerate(line):
            if (x, y) in cartsDict:
                pLine.append(cartsDict[(x, y)].direction)
            else:
                pLine.append(char)

        print("".join(pLine))


def moveCarts(grid, carts):
    carts.sort(key=lambda c: len(grid[1])*c.x + c.y)

    cartMove = {"<": (-1, 0), ">": (1, 0), "v": (0, 1), "^": (0, -1)}

    for cart in carts:
        if (cart.crashed):
            continue

        posDiff = cartMove[cart.direction]

        cart.x += posDiff[0]
        cart.y += posDiff[1]

        # look for crashes
        for other in carts:
            if not cart is other:
                if cart.x == other.x and cart.y == other.y and not other.crashed:
                    cart.crashed = True
                    other.crashed = True

        nextGrid = grid[cart.y][cart.x]

        if nextGrid in "\\/":
            cart.direction = {(">", "/"): "^",
                              (">", "\\"): "v",
                              ("<", "\\"): "^",
                              ("<", "/"): "v",
                              ("^", "\\"): "<",
                              ("^", "/"): ">",
                              ("v", "/"): "<",
                              ("v", "\\"): ">"}[(cart.direction, nextGrid)]
        if nextGrid == "+":
            # left straight right
            cart.direction = {">": "^>v",
                              "<": "v<^",
                              "^": "<^>",
                              "v": ">v<",
                              }[cart.direction][cart.nextTurn]
            cart.nextTurn = (cart.nextTurn + 1) % 3

    crashes = list(filter(lambda x: x.crashed, carts))
    carts = list(filter(lambda x: not x.crashed, carts))

    return crashes, carts


grid, carts = loadFile("day13.txt")

while True:
    crashes, carts = moveCarts(grid, carts)

    if len(carts) == 1:
        print("Last Cart: ", carts[0])
        break
    if crashes:
        print("Crashes: ", crashes)
