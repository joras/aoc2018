
input = "880751"


points = [3, 7]
elfA = 0
elfB = 1
input_int = int(input)
input_arr = list(map(int, input))
i = 0

got1 = False
got2 = False

while True:
    sum = points[elfA] + points[elfB]

    if sum >= 10:
        points.append(sum // 10)
    points.append(sum % 10)

    elfA = (points[elfA] + elfA + 1) % len(points)
    elfB = (points[elfB] + elfB + 1) % len(points)

    if not got2 and (points[-len(input_arr):] == input_arr or points[-len(input_arr)-1:-1] == input_arr):
        print("Solution 2", len(points)-len(input_arr))
        got2 = True

    if not got1 and i == input_int+9:
        got1 = True
        print("Solution 1", "".join(map(str, points[input_int:input_int+10])))

    if got1 and got2:
        break

    i += 1
