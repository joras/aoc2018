import re


def load(filename):

    file = open(filename)
    header = file.readline()
    plants = list(
        map(lambda x: True if x == '#' else False,
            re.findall(r"[#.]+", header)[0]))

    file.readline()

    rules = set()
    for line in file.readlines():
        m = re.match(r"([.#]{5}) => ([.#])", line)

        if m[2] == "#":
            rules.add(tuple(map(lambda x: True if x == '#' else False, m[1])))

    return plants, rules


def grow(plants, rules, startIdx=0):
    res = []

    paddedPlants = [False, False, False] + plants + [False, False, False]

    for i in range(2, len(paddedPlants)-2):
        state = (paddedPlants[i-2],
                 paddedPlants[i-1],
                 paddedPlants[i],
                 paddedPlants[i+1],
                 paddedPlants[i+2])

        if state in rules:
            if not res:
                startIdx = startIdx + i-3
            res.append(True)
        else:
            if res:
                res.append(False)

    return res, startIdx


def plantsStr(plants):
    return "".join(map(lambda x: '#' if x else '.', plants))


plants, rules = load('day12.txt')

idx = 0
previdx = 0
prevplants = []
for i in range(200):
    print(i, idx, plantsStr(plants))
    plants, idx = grow(plants, rules, idx)
    if prevplants == plants:
        print("we're done")
        break
    prevplants = plants

# at this point the pattern does not change, but will move in one direction
# thus we can calculate future index
idx = (50000000000 - i-1) + idx

# sum it
sum = 0
for i, plant in enumerate(plants):
    if plant:
        sum += idx+i

print("Solution 2", sum, i)
