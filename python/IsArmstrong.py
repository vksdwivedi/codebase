import sys

def power(x, y):
    if y == 0:
        return 1
    if y % 2 == 0:
        return power(x, y // 2) * power(x, y // 2)

    return x * power(x, y // 2) * power(x, y // 2)


def order(x):
    n = 0
    while x != 0:
        n = n + 1
        x = x // 10
    return n


def isArmstrong(x):
    n = order(int(x))
    temp = int(x)
    sum1 = 0

    while (temp != 0):
        r = int(temp) % 10
        sum1 = sum1 + power(r, n)
        temp = int(temp) // 10
    return (int(sum1) == int(x))


#for line in sys.stdin:
line = 153
line = isArmstrong(line)
print(line, end="")
