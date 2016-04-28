import random

a = []

while sum(a) < 500:
    a.append(random.randrange(3,6))

a = a[:-1]

print a, sum(a)