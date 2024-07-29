import random

def gera_numeros(range):
    x = random.randint(1, range)
    y = random.randint(1, range)
    z = random.randint(1, range)
    
    w = random.choice([x + y, x + z, y + z])
    
    return (x, y, z, w)

def check_sum(index,numbers):
    sum = 0
    for i in range(3):
        if i != index:
            sum += numbers[i]

    return sum == numbers[3]