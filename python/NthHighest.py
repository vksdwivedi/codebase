def nthHighestsort(list1,n):
    print(list1)
    list1.sort(reverse=True)
    print(list1)
    return list1[n-1]


def nthHighest(list,n):
    final_list = []
    for i in range(n):
        max1 = 0
        for j in range(len(list)):
            a = list[j]
            if a > max1:
                max1 = a
        list.remove(max1)
        final_list.append(max1)

    return final_list[n-1]


a = [342,345,6,76,9,98,23,23,12,1,235,6,67,789,979]
print(nthHighest(a,5))
a = [342,345,6,76,9,98,23,23,12,1,235,6,67,789,979]
print(nthHighestsort(a,5))