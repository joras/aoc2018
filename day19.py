import gc
import re
import time


def load_program(filename):
    ip = 0
    program = []

    for line in open(filename):
        line = line.strip('\n')

        if line.startswith("#ip"):
            ip = int(line.split()[1])
        else:
            l = line.split()
            program.append((l[0], *map(int, l[1:])))

    return ip, program


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


ip, program = load_program("day19.txt")

program = list(map(lambda l: (opcodes[l[0]], (l[1:])), program))

regs = [0] * 6
while True:
    if regs[ip] < 0 or regs[ip] > len(program)-1:
        #print(regs[ip], regs)
        break
    line = program[regs[ip]]
    line[0](regs, *line[1])
    regs[ip] += 1

print("Solution 1", regs[0])


# second half required manual dissasembling
#
# 0 addi 2 16 2  # jump to 17
#
# # init:
# 1  seti 1 1 1  # reg[1] = 1 # step?
# 2  seti 1 8 5  # reg[5] = 1 # count?
#
# loop 1:
#
# check if the multiplication matches the max
# if (reg[1]*reg[5] == reg[3]):
#     reg[0] += reg[1] # add the match to the result

# if not (reg[5]> reg[3]):
#    reg[5]= +1
#    goto loop1
#
# 3  mulr 1 5 4  # reg[4] = reg[1]*reg[5] speed*count
# 4  eqrr 4 3 4  # reg[4] = reg[4] == reg[3]
# 5  addr 4 2 2  # ip = reg[4] + reg[2]
# 6  addi 2 1 2  # ip = ip+1
# 7  addr 1 0 0  # reg[0] = reg[1]+reg[0]
# 8  addi 5 1 5  # reg[5] = reg[5] + 1
# 9  gtrr 5 3 4  # if reg[5] > reg[3]
# 10 addr 2 4 2  # jump to end condition check
# 11 seti 2 0 2  # jump loop1
#
# next block check for end condition:
#
# reg[1] += 1 #raise the step
# if (reg[1]> reg[3]):
#   break
# else:
#  goto loop1
#
#
# 12 addi 1 1 1  # reg[1] + 1
# 13 gtrr 1 3 4  # reg[4] = reg[1]>reg[3]
# 14 addr 4 2 2  # jump to loop
# 15 seti 1 1 2  # jump to loop 1
# 16 mulr 2 2 2  # halt!!!
#
# this block initializes the initial value for reg[3]
# # 17 init reg[3] max:
# 17 addi 3 2 3  # reg[3] += 2
# 18 mulr 3 3 3  # reg[3] *= reg[3]
# 19 mulr 2 3 3  # reg[3] *= reg[2]
# 20 muli 3 11 3 # reg[3] *= 11
# 21 addi 4 7 4  # reg[4] += 7
# 22 mulr 4 2 4  # reg[4] *= reg[2](22)
# 23 addi 4 6 4  # reg[4] += 7
# 24 addr 3 4 3  # reg[3] = reg[3]+reg[4]  # 996
# 25 addr 2 0 2  # skipnext
# 26 seti 0 3 2  # jump to init
# 27 setr 2 0 4  # reg[4] = reg[2](27)
# 28 mulr 4 2 4  # reg[4] = reg[4] * reg[2](28)
# 29 addr 2 4 4  # reg[4] = reg[4] + reg[2](29)
# 30 mulr 2 4 4  # reg[4] = reg[4] * reg[2](30)
# 32 muli 4 14 4 # reg[4] = reg[4] * 14
# 32 mulr 4 2 4  # reg[4] = reg[4] * reg[2](32)
# 33 addr 3 4 3  # reg[3] = reg[3] + reg[4]
#
# # reg[3] = 10551396
# # reg[4] = 10550400
#
# 34 seti 0 4 0  # reg[0] = 0
# 35 seti 0 4 2  # jump to init


# So looking at this, the program calculates a initial value to reg[3]
# And then finds all the factors for this number, and adds factors to the result reg[0]

# so, to find the result, this code as a simplified python

max = 10551396  # reg[3] - the initial value
r = 0  # reg[0] the result
s = 1
while s <= max:
    if max % s == 0:
        r = r+s
    s = s + 1

print("Solution 2", r)
