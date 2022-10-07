"""
Test task
"""
def summ_in_array(array, s):
    pairs=[-1]
    for num1 in array:
        for i in range(array.index(num1), len(array) - 1):
            num2=array[i+1]
            if num1 + num2 == s:
                pairs.append([num1, num2])
    return pairs
