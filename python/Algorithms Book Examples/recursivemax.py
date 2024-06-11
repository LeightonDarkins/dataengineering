def max(list):
    if len(list) < 2:
        if len(list) == 1:
            return list[0]
        else:
            return 0
    else:
        current = list.pop()
        max_from_lower_down = max(list)
        if current > max_from_lower_down:
            return current
        else:
            return max_from_lower_down
        
print(max([5,1,2,9,6,4,144]))