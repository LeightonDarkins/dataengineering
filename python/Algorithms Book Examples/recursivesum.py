def sum(array):
    if len(array) < 2:
        if len(array) == 1:
            return array[0]
        else:
            return 0
    else:
        return array.pop(0) + sum (array)
    
result = sum([1,2,3,4,200])

print(result)