import random
vertices = 100

graph = [[0 for i in xrange(vertices)] for i in xrange(vertices)] 

a = [4, 4, 2, 5, 5, 2, 4, 3, 3, 2, 4, 4, 3, 4, 5, 4, 4, 5, 2, 4, 2, 4, 3, 3, 5, 2, 3, 5]
b = set()

for i in xrange(vertices):
    b.add(i)

output1 = open("solSize100.in", "w")
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


for vertex in xrange(vertices):
    for i in xrange(random.randrange(3*vertices/10,vertices/2)):
        x = random.randrange(0,vertices)
        if x != vertex:
            graph[vertex][x] = 1


output = open("testSize100.in", "w")

output.write("%d\n" %vertices)

children = []
for i in xrange(random.randrange(vertices/4,13*vertices/20)):
    rand = random.randrange(0, vertices)
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




