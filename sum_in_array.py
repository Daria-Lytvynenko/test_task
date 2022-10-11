"""
Test task
"""
def sum_in_array(array, s):
    pairs = []
    for i in array:
        lo = 0
        hi = len(array) - 1
        j = s - i
        while hi > lo:
            mid = (lo + hi) // 2
            if j == array[mid]:
                pairs.append([i, j])
                break
            elif j > array[mid]:
                lo = mid + 1
            else:
                hi = mid
    return pairs
