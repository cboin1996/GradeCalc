def check_weights(lyst, value, total=0):
    for element in lyst:
        total += element[1]
    if total + value <= 1:
        return False
    else:
        return True

def total_weights(lyst, total=0):
    for element in lyst:
        total += element[1]
    return total

def total_product(lyst, total_prod=0):
    for element in lyst:
        total_prod += element[0]*element[1]
    return total_prod


def cast_to_types(lyst):
    return (float(lyst[0]), float(lyst[1]))
