def findSmallestDivisor(s, t):
    # Write your code here
    fits = False
    concat = t
    i = 1
    while len(concat) <= len(s):
        if concat != s:
            i += 1
            concat = t * i
        else:
            fits = True
            break
    if not fits:
        return -1
    for i in range(1, len(t) + 1):
        print(i, t[:i], (len(t) // i), t)
        if (t[:i] * (len(t) // i)) == t:
            return i


if __name__ == "__main__":
    s = "bcdbcdbcdbcd"
    t = "bcdbcd"
    print(findSmallestDivisor(s, t))
