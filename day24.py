import re
import operator as op
import copy


class Group:
    def __init__(self, army, num, units, hp, dmg_type, dmg, weaknesses, immunities, initiative):
        self.army = army
        self.num = num
        self.units = units
        self.hp = hp
        self.dmg_type = dmg_type
        self.dmg = dmg
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.initiative = initiative

    def effective_power(self):
        return self.units * self.dmg

    def calc_damage(self, dmg, dmg_type):
        if dmg_type in self.weaknesses:
            return dmg*2
        if dmg_type in self.immunities:
            return 0

        return dmg

    def take_damage(self, dmg, dmg_type):
        eff_dmg = self.calc_damage(dmg, dmg_type)
        killed = min(self.units, eff_dmg // self.hp)
        self.units -= killed
        return eff_dmg, killed

    def is_dead(self):
        return self.units <= 0

    def __str__(self):
        return f"{self.army}-{self.num} {self.units} with {self.dmg_type}:{self.hp}hp +{self.immunities}"

    def __hash__(self):
        return hash(self.army+str(self.num))


def parse_group(line, army, num):
    weaknesses = []
    immunities = []

    main = re.compile(
        r"(\d+) units each with (\d+) hit points (\(.*\) )?with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)")

    m = main.match(line)
    if not m:
        print(f"cannot parse \"{line}\"")

    if m.group(3):
        wm = re.search(r"weak to ((?:[a-z]+,? ?)+)", m.group(3))
        if wm:
            weaknesses = [i.strip() for i in wm.group(1).split(",")]
        im = re.search(r"immune to ((?:[a-z]+,? ?)+)", m.group(3))
        if im:
            immunities = [i.strip() for i in im.group(1).split(",")]

    return Group(army, num, int(m.group(1)), int(m.group(2)), m.group(5), int(m.group(4)), weaknesses, immunities, int(m.group(6)))


def load_file(filename):
    immune_sys = []
    infection = []
    army = "immune"
    curr = immune_sys
    num = 1

    for line in open(filename).readlines():
        line = line.strip("\n")

        if not line:
            continue

        if line.startswith("Immune System:"):
            pass
        elif line == "Infection:":
            army = "infection"
            curr = infection
            num = 1
        else:
            curr.append(parse_group(line, army, num))
            num += 1

    return infection, immune_sys


def battle(inf, imm):
    units = inf + imm
    pairs = []
    kills = 0
    targeted = set()
    for unit in sorted(units, key=lambda u: (u.effective_power(), u.initiative), reverse=True):
        enemies = list(filter(lambda u: u.army !=
                              unit.army and u not in targeted, units))
        if enemies:
            enemy = max(enemies, key=lambda e: (e.calc_damage(
                unit.effective_power(), unit.dmg_type), e.effective_power(), e.initiative))

            if enemy.calc_damage(unit.dmg, unit.dmg_type) != 0:
                pairs.append((unit, enemy))
                targeted.add(enemy)

    for a, d in sorted(pairs, key=lambda a: a[0].initiative, reverse=True):
        if a.is_dead():
            continue

        _, killed = d.take_damage(a.effective_power(), a.dmg_type)
        kills += killed

    return list(filter(lambda g: not g.is_dead(), inf)), list(filter(lambda g: not g.is_dead(), imm)), kills


def print_state(inf, imm):
    print("Infection army:")
    print("\n".join(map(str, inf)))
    print("Immunity army:")
    print("\n".join(map(str, imm)))


oinf, oimm = load_file("day24.txt")
print_state(oinf, oimm)

boost = 0
while True:
    inf = copy.deepcopy(oinf)
    imm = copy.deepcopy(oimm)

    for g in imm:
        g.dmg += boost

    while inf and imm:
        inf, imm, kills = battle(inf, imm)
        # sometimes we get a tie, nobody can hurt anyone
        if kills == 0:
            break

    if boost == 0:
        print("Solution 1:", sum(map(lambda g: g.units, inf+imm)))

    if imm and not inf:
        print("Solution 2:", sum(map(lambda g: g.units, imm)))
        break

    boost += 1
