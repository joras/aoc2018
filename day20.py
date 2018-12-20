from PIL import Image, ImageDraw


def load_file(filename):
    line = open(filename).readline().strip('\n')[1:-1]

    def parse_direction(dirline, i=0, depth=0):
        steps = []
        options = []

        state = 0
        mdirs = ""

        while i < len(dirline):
            if state == 0:
                cur_chr = dirline[i]

                if cur_chr in "NSWE":
                    mdirs += cur_chr
                elif cur_chr == '(':
                    steps.append(mdirs)
                    mdirs = ""
                    options = []
                    state = 1
                else:
                    if mdirs:
                        steps.append(mdirs)
                        mdirs = ""
                    break
            elif state == 1:
                dirs, plen = parse_direction(dirline, i, depth+1)
                options.append(dirs)
                i = plen

                if dirline[i] == '|':
                    pass
                elif dirline[i] == ')':
                    if options:
                        steps.append(options)
                        state = 0
            i += 1

        if mdirs:
            steps.append(mdirs)

        return steps, i

    steps, _ = parse_direction(line)
    return steps, line


def find_longest_path(directions):
    def walk_path(dirs, depth=0):
        paths = []

        if not dirs:
            return ['']

        for i in dirs:
            if isinstance(i, str):
                if paths:
                    paths = list(map(lambda p: p+i, paths))
                else:
                    paths.append(i)
            else:
                # skip detours if possible
                if [] in i:
                    continue

                subpaths = []
                for option in i:
                    wp = walk_path(option, depth+1)
                    subpaths.extend(wp)

                longest = sorted(subpaths, key=len, reverse=True)[0]

                if paths:
                    new_paths = []
                    for p in paths:
                        new_paths.append(p+longest)
                    paths = new_paths
                else:
                    paths.append(subpaths)

        return paths

    return walk_path(directions)[0]


def find_rooms(directions):
    rooms = {}
    doors = set()

    def walk_path(dirs, step=0, curpos=(0, 0), depth=0):
        for dir in dirs:
            if isinstance(dir, str):
                dirs = {"S": (0, 1), "N": (0, -1), "W": (-1, 0), "E": (1, 0)}
                for d in dir:
                    step += 1
                    diff = dirs[d]
                    prevpos = curpos
                    curpos = (curpos[0]+diff[0], curpos[1]+diff[1])
                    if curpos not in rooms:
                        rooms[curpos] = step
                        doors.add((prevpos, curpos))
                        doors.add((curpos, prevpos))

            else:
                for option in dir:
                    walk_path(option, step, curpos, depth+1)

    walk_path(directions)
    return rooms, doors


directions, line = load_file("day20.txt")

longest_path = find_longest_path(directions)
print("solution 1", len(longest_path))

rooms, doors = find_rooms(directions)
far_rooms = list(filter(lambda x: x >= 1000, rooms.values()))
print("solution 2", len(far_rooms))


# drawing stuff

sx = sorted(rooms, key=lambda r: r[0])
sy = sorted(rooms, key=lambda r: r[1])
min_x = sx[0][0]
max_x = sx[-1][0]
min_y = sy[0][1]
max_y = sy[-1][1]

max_dist = sorted(rooms.values(), reverse=True)[0]

cell_size = 10
wall_size = 1
w, h = max_x-min_x, max_y-min_y
img = Image.new('RGBA', (w*cell_size, h*cell_size), (255, 255, 255, 255))
draw = ImageDraw.Draw(img)

for x in range(min_x, max_x+1):
    line = ""
    for y in range(min_y, max_y+1):
        if (x, y) in rooms:
            ix, iy = (x-min_x)*cell_size, (y-min_y)*cell_size
            dist = rooms[(x, y)]
            cdist = round((dist/max_dist)*255)
            draw.rectangle([ix, iy, ix+cell_size, iy+cell_size],
                           (cdist, 255-cdist, 160, 255))

            if ((x, y), (x, y-1)) not in doors:
                draw.rectangle([ix, iy, ix+cell_size, iy+wall_size],
                               (0, 0, 0, 0))
            if ((x, y), (x, y+1)) not in doors:
                draw.rectangle([ix, iy+cell_size-wall_size, ix+cell_size, iy+cell_size],
                               (0, 0, 0, 0))
            if ((x, y), (x-1, y)) not in doors:
                draw.rectangle([ix, iy, ix+wall_size, iy+cell_size],
                               (0, 0, 0, 0))
            if ((x, y), (x+1, y)) not in doors:
                draw.rectangle([ix+cell_size-wall_size, iy, ix+cell_size, iy+cell_size],
                               (0, 0, 255, 0))

img.show()
