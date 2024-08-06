

def quicksort(list):
    """
    Sorts a list of integers using the quicksort algorithm.

    Parameters:
    list (list): The list of integers to be sorted.

    Returns:
    list: The sorted list of integers.
    """
    if len(list) < 2:
        return list
    else:
        pivot = list[0]
        less = [i for i in list[1:] if i <= pivot]
        greater = [i for i in list[1:] if i > pivot]
        return quicksort(less) + [pivot] + quicksort(greater)

print(quicksort([10,5,2,3]))

