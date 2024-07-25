import random

def gera_numeros():
    x = random.randint(1, 10)
    y = random.randint(1, 10)
    z = random.randint(1, 10)
    
    w = random.choice([x + y, x + z, y + z])
    
    return (x, y, z, w)

def check_sum(index,numbers):
    sum = 0
    for i in range(3):
        if i != index:
            sum += numbers[i]

    return sum == numbers[3]