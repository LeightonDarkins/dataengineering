def count(list):
    if len(list) < 2:
        if len(list) == 1:
            return 1
        else:
            return 0
    else:
        list.pop()
        return 1 + count(list)

print(count([1,2,3,4,5]))
print(count([]))

