def sudoku(size):
    import random as rn
    import sys
    mydict = {}
    n = 0
    while len(mydict) < 9:
        n += 1
        x = range(1, size+1)
        testlist = rn.sample(x, len(x))
        isgood = True
        for dictid,savedlist in mydict.items():
            print("inside for loop")
            if isgood == False:
                break
            for v in savedlist:
                print("value of V:=",v)
                if testlist[savedlist.index(v)] == v:
                    isgood = False
                    break
        if isgood == True:
            #print 'success', testlist
            mydict[len(mydict)] = testlist
    return mydict, n

return_dict, total_tries = sudoku(9)
print(return_dict)
for n,v in return_dict.items():
    print(n,v)
print('in',total_tries,'tries')
