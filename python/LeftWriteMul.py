def leftwritemul(lst):
    length = len(lst)
    llist = [0]*length
    rlist = [0]*length
    prod = [0]*length
    print(rlist)
    llist[0] = 1
    rlist[length-1] = 1

    for i in range(1,length):
        llist[i] = llist[i-1]*lst[i-1]
    print(llist)
    for j in range(length-2, -1, -1):
        print(j,lst[j + 1],rlist[j + 1])
        rlist[j] = lst[j + 1] * rlist[j + 1]

    for k in range(length):
        prod[k] = llist[k]*rlist[k]
    print(prod)

def mulproduct(lst):
    mul = 1
    prod = [0]*len(lst)
    for i in range(len(lst)):
        mul = mul*lst[i]

    for j in range(len(lst)):
        prod[j] = int(mul/lst[j])
    print(prod)

a =[1,2,3,4,5]
#leftwritemul(a)
mulproduct(a)