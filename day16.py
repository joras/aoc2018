import re

file = open("day16.txt")

tests = []
program = []

digit = re.compile(r"\d+")
while True:
    line = file.readline()
    if not line:
        break

    line = line.strip('\n')

    if line.startswith("Before"):
        test = (
            list(map(int, digit.findall(line))),
            tuple(map(int, digit.findall(file.readline()))),
            list(map(int, digit.findall(file.readline()))))

        tests.append(test)
    elif line:
        program.append(map(int, digit.findall(line)))


def addr(state, a, b, c):
    state[c] = state[a]+state[b]


def addi(state, a, b, c):
    state[c] = state[a]+b


def mulr(state, a, b, c):
    state[c] = state[a]*state[b]


def muli(state, a, b, c):
    state[c] = state[a]*b


def banr(state, a, b, c):
    state[c] = state[a] & state[b]


def bani(state, a, b, c):
    state[c] = state[a] & b


def borr(state, a, b, c):
    state[c] = state[a] | state[b]


def bori(state, a, b, c):
    state[c] = state[a] | b


def setr(state, a, b, c):
    state[c] = state[a]


def seti(state, a, b, c):
    state[c] = a


def gtir(state, a, b, c):
    state[c] = 1 if a > state[b] else 0


def gtri(state, a, b, c):
    state[c] = 1 if state[a] > b else 0


def gtrr(state, a, b, c):
    state[c] = 1 if state[a] > state[b] else 0


def eqir(state, a, b, c):
    state[c] = 1 if a == state[b] else 0


def eqri(state, a, b, c):
    state[c] = 1 if state[a] == b else 0


def eqrr(state, a, b, c):
    state[c] = 1 if state[a] == state[b] else 0


opcodes = [addr, addi, mulr, muli, banr, bani,
           borr, bori, setr, seti, gtri, gtir, gtrr, eqir, eqri, eqrr]

print("opcodes:", len(opcodes))
# exit()

# run tests
res = []
for state, command, result in tests:
    matching = []
    # print(state, command, result)

    for opcode in opcodes:
        teststate = state.copy()
        opcode(teststate, *command[1:])
        if teststate == result:
            matching.append(opcode)

    res.append((command[0], matching))

m = list(filter(lambda r: len(r[1]) >= 3, res))
print("solution 1:", len(m))

commands = {k: v[0] for (k, v) in filter(lambda r: len(r[1]) == 1, res)}

nonunique = list(filter(lambda r: len(r[1]) > 1, res))
nonunique.sort(key=lambda p: len(p[1]), reverse=True)

reversemap = dict()
for instr, cmds in nonunique:
    for c in cmds:
        if c in commands.values():
            continue
        if c in reversemap:
            reversemap[c].add(instr)
        else:
            reversemap[c] = set()
            reversemap[c].add(instr)

while reversemap:
    match = None

    for cmd in reversemap.keys():
        known_ids = commands.keys()
        ids = reversemap[cmd]
        ids = ids.difference(known_ids)
        reversemap[cmd] = ids

        if len(ids) == 1:
            match = (ids.pop(), cmd)
            break

    if match:
        id, cmd = match
        commands[id] = cmd
        del reversemap[cmd]


print("instruction set:", commands)

state = [0]*4
for instr, a, b, c in program:
    commands[instr](state, a, b, c)

print(state)
