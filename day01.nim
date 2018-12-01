import parseUtils
import setS

proc parseToNums(fileName: string): seq[int] =
  for i in lines(fileName):
    var val = 0
    discard parseInt(i, val)
    result.add(val)

proc solve1(numbers: seq[int]): int =
  for num in numbers:
    result += num;


proc solve2(numbers: seq[int]): int =
  var freqs = initSet[int](rightSize(numbers.len*10))
  var sum = 0

  while true:
    for i in numbers:
      if freqs.containsOrIncl(sum):
        return sum
      sum += i;





let inputData = parseToNums("day01.txt")

# solution 1
echo "solution 1: ", solve1(inputData)

# solution 2
assert solve2(@[+3, +3, +4, -2, -4]) == 10;
echo "solution 2: ",solve2(inputData)