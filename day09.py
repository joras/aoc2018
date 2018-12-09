from timeit import default_timer as timer
from dataclasses import dataclass


class CircularList:
    @dataclass
    class Node:
        value: int
        left: object
        right: object

    def __init__(self):
        self.currNode = None

    def currValue(self):
        if self.currNode is None:
            return None
        else:
            return self.currNode.value

    def seek(self, amount):
        if self.currNode is None:
            return self

        for _ in range(abs(amount)):
            if amount < 0:
                self.currNode = self.currNode.left
            else:
                self.currNode = self.currNode.right

        return self

    def pop(self):
        if self.currNode is None:
            return None
        elif self.currNode.left is self.currNode.right:
            val = self.currNode.value
            self.currNode = None
            return val
        else:
            self.currNode.left.right = self.currNode.right
            self.currNode.right.left = self.currNode.left
            val = self.currNode.value
            self.currNode = self.currNode.right
            return val

    def insert(self, value):
        if self.currNode is None:
            self.currNode = self.Node(value, None, None)
            self.currNode.left = self.currNode
            self.currNode.right = self.currNode
        else:
            newNode = self.Node(
                value, self.currNode, self.currNode.right)

            self.currNode.right.left = newNode
            self.currNode.right = newNode

            self.currNode = newNode

    def tolist(self):
        if self.currNode is None:
            return []
        else:
            res = []
            nextNode = self.currNode

            while True:
                res.append(nextNode.value)
                nextNode = nextNode.right

                if nextNode == self.currNode:
                    return res

    def __str__(self):
        return str(self.tolist())


def playgames(numberOfElves, biggestMarble):
    marbleCircle = CircularList()
    marbleCircle.insert(0)

    elves = [0] * numberOfElves
    elveIdx = 0

    for marbleValue in range(1, biggestMarble+1):
        if marbleValue % 23 == 0:
            elves[elveIdx] += marbleValue
            elves[elveIdx] += marbleCircle.seek(-7).pop()
        else:
            marbleCircle.seek(1).insert(marbleValue)

        elveIdx = (elveIdx + 1) % numberOfElves

    return elves


start = timer()
print("Solution 1", max(playgames(468, 71010)))
end = timer()
print("   Time: ", end - start)

start = timer()
print("Solution 2", max(playgames(468, 71010*100)))
end = timer()
print("   Time: ", end - start)
