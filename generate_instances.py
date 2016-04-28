import random

graph = [[0 for i in xrange(500)] for i in xrange(500)] 

a = [3, 3, 4, 4, 3, 5, 5, 4, 4, 4, 5, 3, 3, 5, 5, 5, 4, 5, 5, 3, 5, 5, 4, 5, 3, 3, 4, 5, 5, 5, 5, 3, 4, 5, 3, 3, 4, 3, 3, 4, 3, 4, 4, 4, 4, 5, 3, 5, 3, 5, 5, 5, 3, 5, 3, 5, 3, 3, 3, 4, 4, 5, 4, 4, 5, 5, 3, 5, 3, 4, 5, 4, 3, 4, 4, 5, 4, 3, 3, 4, 5, 4, 3, 3, 3, 5, 5, 3, 4, 3, 3, 5, 3, 3, 3, 3, 4, 5, 5, 3, 3, 3, 5, 5, 5, 3, 5, 3, 3, 5, 4, 5, 5, 4, 5, 3, 4, 3, 4, 4, 5, 3, 5, 5, 3]

b = set()

for i in xrange(500):
    b.add(i)

output1 = open("sol1.in", "w")
for cycle in a:
    vertex = random.sample(b, cycle)
    for index in range(0, len(vertex)):
        b.remove(vertex[index])
        if index != len(vertex) -1:
            graph[vertex[index]][vertex[index+1]] = 1
        else:
            graph[vertex[index]][vertex[0]] = 1
    output1.write(str(vertex) + "\n")
output1.close()


for vertex in xrange(500):
    for i in xrange(random.randrange(150,250)):
        x = random.randrange(0,500)
        if x != vertex:
            graph[vertex][x] = 1


output = open("BretzelsAndChestnuts1.in", "w")

output.write("500\n")

children = []
for i in xrange(random.randrange(125,325)):
    rand = random.randrange(0, 500)
    if rand not in children:
        children.append(rand)

children = sorted(children)

for child in children:
    output.write("%d " %child)

output.write("\n")


for item in graph:
    for vertex in item:
        output.write("%d " %vertex)
    output.write("\n")


output.close()




