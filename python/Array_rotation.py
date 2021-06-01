def reverseArray(arr, start, end):
    temp = [None] * end
    for i in range(end):
        if i+start >= end:
            idx = (i+start) - end
        else:
            idx = i+start
        temp[i] = arr[idx]
    return temp




def leftRotate(arr, d):
    if d == 0:
        return
    n = len(arr)
    d = d % n
    if d == 0:
        return arr
    return reverseArray(arr, d, n)





# Driver function to test above functions
arr = [1, 2, 3, 4, 5, 6, 7]
n = len(arr)
d = 8

print(leftRotate(arr, d))  # Rotate array by 2
#printArray(arr)