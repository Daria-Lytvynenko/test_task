"""
Test task
"""

def lucky (numbers):
    combination = re.split('[0-4, 7-9]', str(numbers))
    combination = [i for i in combination if len(set(i)) != 1 and len(set(i)) != 0]
    try:
        result = max(combination, key=len)
        return result
    except ValueError:
        return 0
