import random
from copy import copy, deepcopy

source_file = "phase1-processed/130.in"
print("Starting file: " + source_file)
instance = open(source_file, "r")

vertices = int(instance.readline())
#kids = instance.readline()
#kids = []
kids = map(int, instance.readline().strip().split(" "))
print kids
matrix = [[0 for i in xrange(vertices)] for i in xrange(vertices)]

for i in xrange(vertices):
	matrix[i] = map(int, instance.readline().strip().split(" "))
originalMatrix = deepcopy(matrix)

def get_children(v):
	children = []
	for child in xrange(vertices):
		if matrix[v][child] == 1: 
			children.append(child)
	#print "Children found for %d." %v
	return children

def rotate_lowest(l):
	lowest = min(l)
	while l[0] != lowest:
		l = l[-1:] + l[:-1]
	return l




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

def allCyclesMethod():
	cycles = []
	for vertex in xrange(vertices): # for each vertex
		for child in get_children(vertex):
			curr_path = [vertex]
			explore(child, curr_path[:], cycles)


	print cycles

def checkValid(soln):
	for item in soln:
		for i in xrange(len(item)):
			if i == len(item)-1:
				if originalMatrix[item[i]][item[0]] != 1:
					print "error2: ", item
			else:
				if originalMatrix[item[i]][item[i+1]] != 1:
					print "error1: ", item

greedyFlag = False

def setFlagTrue():
	global greedyFlag
	greedyFlag = True

def setFlagFalse():
	global greedyFlag
	greedyFlag = False

def checkFlag():
	return greedyFlag

def getKids():
	return kids

def greedyExplore(vertex, curr_path, cycles):
	#print "starting explore for current path " + str(curr_path) + " and vertex %d" %vertex
	if len(curr_path) > 5 or checkFlag():
		return
	if vertex == curr_path[0]:
		curr_path = rotate_lowest(curr_path)
		if curr_path not in cycles:
			cycles.append(curr_path[:])
			setFlagTrue()
		return
	if vertex in curr_path:
		return
	children = get_children(vertex)
	for child in children:
		#print "finding children of vertex:", vertex, child
		curr_path2 = curr_path[:]
		curr_path2.append(vertex)
		greedyExplore(child, curr_path2, cycles)

def greedyMethod():
	print "Starting Greedy Strategy..."
	nodes = set()
	answer = []
	kidDonors = getKids()
	for i in xrange(vertices):
		nodes.add(i)
	while nodes:
		if kidDonors:
			rand = random.randrange(0, len(kidDonors))
			currNode = kidDonors.pop(rand)
		else:
			currNode = random.sample(nodes, 1)[0]
		#currNode = random.sample(nodes, 1)[0]
		print "Analyzing node %d" %currNode
		print "%d out of %d nodes left." %(len(nodes),vertices)
		cycles = []
		for child in get_children(currNode):
			curr_path = [currNode]
			setFlagFalse()
			greedyExplore(child, curr_path[:], cycles)
		cycles = sorted(cycles, key = len)
		if len(cycles) == 0:
			nodes.remove(currNode)
		else:
			bestCycle = cycles[-1]
			for item in bestCycle:
				if item in kidDonors:
					kidDonors.remove(item)
				nodes.remove(item)
				for i in xrange(vertices):
					matrix[i][item] = 0
			answer.append(bestCycle)
	return answer

solution = greedyMethod()
total = 0
for item in solution:
	total += len(item)
print "Solution is: ", solution
print "Total vertices covered: ", total, "/ %d" %vertices
checkValid(solution)
#allCyclesMethod()

