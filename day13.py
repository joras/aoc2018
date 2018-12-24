from dataclasses import dataclass
from PIL import Image, ImageDraw


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
        curLine = []
        for x, char in enumerate(line.strip('\n')):
            cartChar = "<>v^"
            if char in cartChar:
                carts.append(Cart(char, x, y, 0, False))
                curLine.append("--||"[cartChar.find(char)])
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



def renderImage(grid, carts, crashes):
    cell_size = 5
    w, h = len(grid[0]), len(grid)
    img = Image.new('RGBA', (w*cell_size, h*cell_size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    track_color = (100, 100, 100, 255)

    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            #    print(y, x)
            gx = x*cell_size
            gy = y*cell_size

            if char == '|':
                draw.line([(gx+2, gy), (gx+2, gy+4)], track_color)
            elif char == '-':
                draw.line([(gx, gy+2), (gx+4, gy+2)], track_color)
            elif char == '/':
                if y < h-1 and grid[y+1][x] in "|+":
                    draw.line([(gx+2, gy+4), (gx+2, gy+2), (gx+4, gy+2)],
                              track_color)
                if y > 0 and grid[y-1][x] in "|+":
                    draw.line([(gx, gy+2), (gx+2, gy+2), (gx+2, gy)],
                              track_color)
            elif char == '\\':
                if y < h-1 and grid[y+1][x] in '|+':
                    draw.line([(gx, gy+2), (gx+2, gy+2), (gx+2, gy+4)],
                              track_color)
                if y > 0 and grid[y-1][x] in '|+':
                    draw.line([(gx+2, gy), (gx+2, gy+2), (gx+4, gy+2)],
                              track_color)

            elif char == '+':
                draw.line([(gx+2, gy), (gx+2, gy+4)], track_color)
                draw.line([(gx, gy+2), (gx+4, gy+2)], track_color)

    for cart in crashes:
        gx, gy = cart.x*cell_size, cart.y*cell_size
        draw.rectangle([(gx+1, gy+1),
                        (gx+3, gy+3)], (200, 100, 100, 255))
        draw.line([(gx, gy), (gx+4, gy+4)], (200, 100, 100, 255))
        draw.line([(gx+4, gy), (gx, gy+4)], (200, 100, 100, 255))

    for cart in carts:
        draw.rectangle([(cart.x*cell_size+1, cart.y*cell_size+1),
                        (cart.x*cell_size+3, cart.y*cell_size+3)], (100, 100, 250, 255))

    return img


grid, carts = loadFile("day13.txt")


printNetwork(grid, carts)
img = renderImage(grid, carts, [])
img.show()

allCrashes = []
i = 0
while True:
    crashes, carts = moveCarts(grid, carts)
    allCrashes.extend(crashes)
    img = renderImage(grid, carts, allCrashes)
    img.save(f"animation/frame{i:06}.png")
    i += 1

    if len(carts) == 1:
        print("Last Cart: ", carts[0])
        break
    if crashes:
        img.show()
        print("Crashes: ", crashes)

    img.close()
