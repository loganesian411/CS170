import random
from copy import copy, deepcopy
from collections import defaultdict
from math import ceil
from collections import Counter

#source_file = "phase1-processed/10.in"
source_file = "phase1-processed/344.in"
print("Starting file: " + source_file)
instance = open(source_file, "r")

vertices = int(instance.readline())
kids = instance.readline()
# kids = []
# kids = map(int, instance.readline().strip().split(" "))
matrix = [[0 for i in xrange(vertices)] for i in xrange(vertices)]

for i in xrange(vertices):
	matrix[i] = map(int, instance.readline().strip().split(" "))
originalMatrix = deepcopy(matrix)

def get_children(v):
	global children
	return children[v]

def cachechildren():
	children = defaultdict(list)
	for v in xrange(vertices):
		for child in xrange(vertices):
			if matrix[v][child] == 1:
				children[v].append(child)
	return children

def rotate_lowest(l):
        lowestind = l.index(min(l))
        l = l[lowestind:]+l[:lowestind]
        return l

def explore(vertex, curr_path, cycles):
	#print "starting explore:", vertex, curr_path, cycles
	if len(curr_path) > 5:
		return
	if vertex == curr_path[0]:
		curr_path = rotate_lowest(curr_path)
		if curr_path not in cycles[curr_path[0]]:
			cycles[curr_path[0]].append(curr_path[:])
		return
	if vertex in curr_path:
		return
	curr_path.append(vertex)
	for child in get_children(vertex):
		explore(child, curr_path, cycles)
	curr_path.pop()

def allCyclesMethod():
	cycles = defaultdict(list)
	for vertex in xrange(vertices):
		curr_path = [vertex]
		print 'new vertex'
		for child in get_children(vertex):
                        explore(child, curr_path, cycles)
	print cycles
	return cycles



def allCyclesMethodRandomized(fracVert=0.3, maxCycles=50):
	cycles = defaultdict(list)
	numFound = Counter()
	for vertex in xrange(vertices):
		if len(cycles[vertex]) >= maxCycles:
			continue
		curr_path = [vertex]
		print 'new vertex {0}'.format(vertex)
		vert_children = get_children(vertex)
		childrenToConsider = int(ceil(fracVert*len(vert_children)))
		random.shuffle(vert_children)
		for child in vert_children[:childrenToConsider]:
			print 'exploring child {0}'.format(child)
                        exploreRandom(child, curr_path, cycles, maxCycles, fracVert, numFound)
	print cycles
	return cycles

def exploreRandom(vertex, curr_path, cycles, maxCycles, fracVert, numFound):
	#if len(curr_path) == 5 and vertex != curr_path[0]:
	#	return
	if vertex == curr_path[0]:
		tmp = rotate_lowest(curr_path)
		if tmp not in cycles[tmp[0]]:
			cycles[tmp[0]].append(tmp)
		numFound[curr_path[0]] += 1
		return
	if numFound[curr_path[0]] >= maxCycles:
		print 'exiting {0}'.format(numFound[curr_path[0]])
		return
	if vertex in curr_path:
		halfpath = curr_path[curr_path.index(vertex):]
		if halfpath not in cycles[vertex]:
			cycles[vertex].append(halfpath)
	if numFound[vertex] >= maxCycles:
		return
	curr_path.append(vertex)
	vert_children = get_children(vertex)
	childrenToConsider = int(ceil(fracVert*len(vert_children)))
	random.shuffle(vert_children)
	for child in vert_children[:childrenToConsider]:
		if len(curr_path) == 5 and child != curr_path[0]:
			continue
		print 'cp {0}, child {1}'.format(curr_path, child)
		exploreRandom(child, curr_path, cycles, maxCycles, fracVert, numFound)
	curr_path.pop()

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
	for i in xrange(vertices):
		nodes.add(i)
	while nodes:
		currNode = random.sample(nodes, 1)[0]
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
				nodes.remove(item)
				for i in xrange(vertices):
					matrix[i][item] = 0
			answer.append(bestCycle)
	return answer

#solution = greedyMethod()
#solution = allCyclesMethod()
children = cachechildren()
solution = allCyclesMethodRandomized()
total = 0
vertscovered = set()
for key in solution.keys():
	total += len(solution[key])
	for cycle in solution[key]:
		vertscovered.update(cycle)
#for item in solution:
#	total += len(item)
print "Solution is: ", solution
print 'Number of cycles found: {0}'.format(total)
print "Total vertices covered: ", len(vertscovered), "/ %d" %vertices
#checkValid(solution)

#allCyclesMethod()
# 344 352 369 409 413 418 429 and 452 
