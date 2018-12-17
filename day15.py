import numpy as np
from dataclasses import dataclass
from collections import deque, namedtuple


@dataclass
class Monster:
    x: int
    y: int
    type: str
    hp: int


def load_file(filename):

    grid = []
    monsters = []

    f = open(filename)
    for y, line in enumerate(f.readlines()):
        n_line = ""
        for x, char in enumerate(line):
            if char in "GE":
                monsters.append(Monster(x, y, char, 200))
                n_line += "."
            elif char in "#.":
                n_line += char
        grid.append(n_line)

    f.readline()
    f.close()

    return grid, monsters


class Dungeon:
    def __init__(self, grid, monsters):
        self.grid = grid
        self.__w = len(grid[0])
        self.__h = len(grid)
        self.update_monsters(monsters)
        pass

    def update_monsters(self, monsters):
        self.monsters = monsters
        self.monsters.sort(key=lambda m: m.y * self.__h + m.x)
        self._mlocs = {(m.x, m.y): m for m in monsters}

    def __getitem__(self, t):
        x = t[0]
        y = t[1]

        if x < 0 or x > self.__w - 1:
            return "#"

        if y < 0 or y > self.__h - 1:
            return "#"

        if (x, y) in self._mlocs:
            return self._mlocs[(x, y)]
        else:
            return self.grid[y][x]

    def __str__(self):
        out = ""

        for y in range(self.__h):
            monsters = " "
            for x in range(self.__w):
                c = self[x, y]
                if type(c) is Monster and c.hp > 0:
                    out += c.type
                    monsters += f"{c.type}({c.hp}) "
                else:
                    out += c
            out += monsters + '\n'

        return out

    def paths_to_enemies(self, m):
        enemies = []

        def step_to_enemy(loc, prevsteps):
            for dir in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
                nextloc = (loc[0] + dir[0], loc[1] + dir[1])

                if nextloc in prevsteps:
                    continue

                nextcell = self[nextloc]
                # print(loc, nextloc, nextcell)

                if type(nextcell) is Monster:
                    if nextcell.type != m.type:
                        enemies.append((prevsteps, nextcell))
                        return
                    else:
                        continue

                if nextcell == '.':
                    step_to_enemy(nextloc, prevsteps + [nextloc])
                else:
                    continue

        step_to_enemy((m.x, m.y), [])
        return enemies

    def bfspaths_to_enemies(self, m):
        enemy_loc = []

        seen = set([(m.x, m.y)])
        front = deque([((m.x, m.y), None, 0)])
        #found = False

        while front:
            loc, prev, depth = front.popleft()
            # visited.add(loc)
           # print("visited: ", len(seen), len(front))

            for dir in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
                nextloc = (loc[0] + dir[0], loc[1] + dir[1])

                # if nextloc
                if nextloc in seen:
                    continue

                seen.add(nextloc)
                cell = self[nextloc]
                if type(cell) is Monster and cell.type != m.type:
                    enemy_loc.append(((loc, prev, depth), cell))
                    found = True
                elif cell == '.':
                    # if loc not in seen:
                    front.append((nextloc, (loc, prev, depth), depth+1))

            # visited.add(loc)
            # print(visited)

        enemies = []
        for eloc in enemy_loc:

            location, enemy = eloc

           # print("eloc", eloc)
            path = []
            curloc = location
            while True:
                if not curloc[1]:
                    break
                path.append(curloc[0])
                curloc = curloc[1]

            path.reverse()
            enemies.append((enemy, path))

        return enemies

    def simulate_step(self, elvepower=3):
        dungeon.monsters.sort(
            key=lambda currmonster: currmonster.y * self.__w + currmonster.x)

        def weakest_in_range(m):
            enemies = []

            for dir in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
                loc = m.x+dir[0], m.y + dir[1]
                if loc in self._mlocs and self._mlocs[loc].type != m.type:
                    enemies.append(self._mlocs[loc])

            if enemies:
                enemies.sort(key=lambda x: x.hp)
                return enemies[0]

            return None

        def path_order(path_to_enemy):
            path = path_to_enemy[1]
            order = len(path) * self.__w * self.__h
            if path:
                lastpos = path[-1]
                order += self.__w * lastpos[1] + lastpos[0]
            return order

        monsters_to_move = self.monsters.copy()
        while monsters_to_move:
            currmonster = monsters_to_move.pop(0)
           # print("curr", currmonster)

            if currmonster not in self.monsters:
                continue

            # find paths to monsters
            paths = self.bfspaths_to_enemies(currmonster)
            paths.sort(key=path_order)

            # print(paths)
            if paths:
                shortestPath = paths[0][1]
               # closestEnemy = paths[0][0]

               # print("shortest", currmonster, shortestPath)
                if shortestPath:
                    currmonster.x = shortestPath[0][0]
                    currmonster.y = shortestPath[0][1]

            enemy_to_hit = weakest_in_range(currmonster)
            if enemy_to_hit:
              #  print("enemy in range", closestEnemy)
                hit = elvepower if currmonster.type == "E" else 3
                #print("hitting with: ", hit)
                enemy_to_hit.hp -= hit
                if enemy_to_hit.hp <= 0:
                    if enemy_to_hit in monsters_to_move:
                        monsters_to_move.remove(enemy_to_hit)
                    if enemy_to_hit in self.monsters:
                        self.monsters.remove(enemy_to_hit)
                    self.update_monsters(self.monsters)
               #
               #
            self.update_monsters(self.monsters)

        # def simulate_step(self):


grid, monsters = load_file("day15.txt")
step = 0
dungeon = Dungeon(grid.copy(), monsters.copy())
while True:
    dungeon.simulate_step()
    print("step:", step)
    print(dungeon)

    goblins = list(filter(lambda m: m.type == "G", dungeon.monsters))
    elves = list(filter(lambda m: m.type == "E", dungeon.monsters))

    # print(dungeon.monsters)
    #print(len(dungeon.monsters), len(goblins), len(elves))
    if not goblins or not elves:
        print("Solution 1: ", sum(map(lambda x: x.hp, dungeon.monsters)) * step)
        break

    step += 1


elvepower = 3
found = False


while not found:

    grid, monsters = load_file("day15.txt")
    dungeon = Dungeon(grid.copy(), monsters.copy())
    origElves = len(list(filter(lambda m: m.type == "E", dungeon.monsters)))
    elvepower += 1

    step = 0
    print("elvePower", elvepower)
    while True:
        dungeon.simulate_step(elvepower)
        #print("step:", step)
        # print(dungeon)

        goblins = list(filter(lambda m: m.type == "G", dungeon.monsters))
        elves = list(filter(lambda m: m.type == "E", dungeon.monsters))

        if len(elves) < origElves:
            print("fight failed")
            break

        # print(dungeon.monsters)
        #print(len(dungeon.monsters), len(goblins), len(elves))
        if not goblins:
            print("Solution2: ", sum(map(lambda x: x.hp, dungeon.monsters)) * step)
            found = True
            break

        step += 1

# for monster in
# print(grid, monsters)
# print(dungeon)
