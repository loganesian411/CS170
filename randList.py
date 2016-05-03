import random

a = []

while sum(a) < 100:
    a.append(random.randrange(2,6))

a = a[:-1]

print a, sum(a)