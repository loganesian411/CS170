source_file = "phase1-processed/300.in"
print("Starting file: " + source_file)
instance = open(source_file, "r")

vertices = int(instance.readline())
kids = instance.readline()
# kids = []
# kids = map(int, instance.readline().strip().split(" "))
matrix = [[0 for i in xrange(vertices)] for i in xrange(vertices)]

for i in xrange(vertices):
	matrix[i] = map(int, instance.readline().strip().split(" "))

def get_children(v):
	children = []
	for child in xrange(vertices):
		if matrix[v][child] == 1: 
			children.append(child)
	return children

def rotate_lowest(l):
	lowest = min(l)
	while l[0] != lowest:
		l = l[-1:] + l[:-1]
	return l

cycles = []

def explore(vertex, curr_path, cycles):
	#print "starting explore:", vertex, curr_path, cycles
	if len(curr_path) > 5:
		return
	if vertex == curr_path[0]:
		curr_path = rotate_lowest(curr_path)
		if curr_path not in cycles:
			cycles.append(curr_path[:])
		return
	if vertex in curr_path:
		return
	for child in get_children(vertex):
		#print "finding children of vertex:", vertex, child
		curr_path2 = curr_path[:]
		curr_path2.append(vertex)
		explore(child, curr_path2, cycles)


for vertex in xrange(vertices): # for each vertex
	for child in get_children(vertex):
		curr_path = [vertex]
		explore(child, curr_path[:], cycles)


print cycles

for item in cycles:
	for i in xrange(len(item)):
		if i == len(item)-1:
			if matrix[item[i]][item[0]] != 1:
				print "error2"
		else:
			if matrix[item[i]][item[i+1]] != 1:
				print "error1"
print "okay"

