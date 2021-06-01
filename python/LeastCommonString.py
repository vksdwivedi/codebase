def LCSubStr(X, Y, m, n):
    LCStuff = [[0 for k in range(n + 1)] for l in range(m + 1)]
    result = 0
    for i in range(m + 1):
        for j in range(n + 1):
            if i != 0 and j != 0:
                print("CHK:= ",i,j,X[i - 1],Y[j - 1])
            if i == 0 or j == 0:
                print(i,j,LCStuff)
                LCStuff[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                LCStuff[i][j] = LCStuff[i - 1][j - 1] + 1
                print(i,j,LCStuff)
                result = max(result, LCStuff[i][j])
            else:
                LCStuff[i][j] = 0
    return result


# Driver Code
X = 'vika'
Y = 'ik'

m = len(X)
n = len(Y)

print(LCSubStr(X, Y, m, n))
