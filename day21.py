import gc
import re
import time


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


opcodes = {"addr": addr,
           "addi": addi, "mulr": mulr, "muli": muli, "banr": banr, "bani": bani,
           "borr": borr, "bori": bori, "setr": setr, "seti": seti, "gtri": gtri, "gtir": gtir, "gtrr": gtrr, "eqir": eqir, "eqri": eqri, "eqrr": eqrr}


def load_program(filename):
    ip = 0
    program = []

    for line in open(filename):
        line = line.strip('\n')
        if not line:
            continue

        if line.startswith("#ip"):
            ip = int(line.split()[1])
        elif not line.startswith("#"):
            c = line.find("#")
            if c != -1:
                line = line[:c]
            l = line.split()
            program.append((l[0], *map(int, l[1:])))

    return ip, list(map(lambda l: (opcodes[l[0]], (l[1:])), program))


ip, program = load_program("day21.txt")


def print_inst_exec(command, params, regs, prev_regs):
    line_no = str(prev_regs[ip])
    raw = command.__name__ + " " + ", ".join(map(str, params))

    cmd = command.__name__

    a, b, c = params
    decoded = ""
    evald = ""

    def regname(r): return f"r{r}" if r != ip else "ip"

    rn = list(map(regname, range(6)))

    if command == addr:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) + {rn[b]}({prev_regs[b]}) = {regs[c]}"
    elif command == addi:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) + {b} = {regs[c]}"
    if command == mulr:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) * {rn[b]}({prev_regs[b]}) = {regs[c]}"
    elif command == muli:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) * {b} = {regs[c]}"
    elif command == banr:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) & {rn[b]}({prev_regs[b]}) = {regs[c]}"
    elif command == bani:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) & {b} = {regs[c]}"
    elif command == borr:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) | {rn[b]}({prev_regs[b]}) = {regs[c]}"
    elif command == bori:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) | {b} = {regs[c]}"
    elif command == setr:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) "
    elif command == seti:
        decoded = f"{rn[c]} = {a}"
    elif command == gtrr:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) > {rn[b]}({prev_regs[b]}) = {regs[c]}"
    elif command == gtri:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) > {b} = {regs[c]}"
    elif command == gtri:
        decoded = f"{rn[c]} = {a} > {rn[b]}({prev_regs[b]}) = {regs[c]}"
    elif command == eqrr:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) == {rn[b]}({prev_regs[b]}) = {regs[c]}"
    elif command == eqri:
        decoded = f"{rn[c]} = {rn[a]}({prev_regs[a]}) == {b} = {regs[c]}"
    elif command == eqri:
        decoded = f"{rn[c]} = {a} == {rn[b]}({prev_regs[b]}) = {regs[c]}"

# "gtri": gtri, "gtir": gtir, "gtrr": gtrr, "eqir": eqir, "eqri": eqri, "eqrr": eqrr

    rs = "["+", ".join(map(str, regs))+"]"
    line_no = line_no + " "*(4-len(line_no))
    raw = raw + " "*(25-len(raw))
    decoded = "\033[1;37m" + decoded + " "*(45-len(decoded)) + "\033[0m"
    print(line_no + raw + decoded + rs)


regs = [0] * 6

nums = set()
prev = 0

debug = True
i = 0

while True:
    if i > 100:
        break

    # from reading the elfcode, we know that the exit comparison happens
    # at line 28. and when the value is equal to r3
    if regs[ip] == 28:
        if not nums:
            # first match, solution 1
            print("Solution 1", regs[3])
        if regs[3] not in nums:
            nums.add(regs[3])
            prev = regs[3]
        else:
            # found the cycle, the previous value is the answer
            print("Solution 2", prev)
            break

    command, params = program[regs[ip]]
    if debug:
        prev_regs = regs.copy()
    command(regs, *params)

    if debug:
        print_inst_exec(command, params, regs, prev_regs)

    regs[ip] += 1
    i += 1
