def binary_search(list, guess):
    if len(list) < 2:
        if len(list) == 1:
            if list[0] == guess:
                return list[0]
            else:
                return -1
        else:
            return -1
    else:
        mid_point = int(len(list) / 2)
        if (list[mid_point] > guess):
            return binary_search(list[:mid_point], guess)
        else:
            return binary_search(list[mid_point:], guess)

print(binary_search([1,2,3,4,5], 3))
print(binary_search([1,2,3,4,5], 7))