import random
from copy import copy, deepcopy
from collections import defaultdict
from math import ceil
from collections import Counter

# source_file = "phase1-processed/10.in"
# source_file = "phase1-processed/344.in"
source_file = "phase1-processed/112.in"
# source_file = 'phase1-processed/119.in'

print("Starting file: " + source_file)
instance = open(source_file, "r")

vertices = int(instance.readline())

#kids = instance.readline()
kids = map(int, instance.readline().strip().split(" "))

# kids = []
# kids = map(int, instance.readline().strip().split(" "))
matrix = [[0 for i in xrange(vertices)] for i in xrange(vertices)]

for i in xrange(vertices):
	matrix[i] = map(int, instance.readline().strip().split(" "))
originalMatrix = deepcopy(matrix)

# def get_children(v):
# 	global children
# 	return children[v]

def get_children(v):
	children = []
	for child in xrange(vertices):
		if matrix[v][child] == 1: 
			children.append(child)
	#print "Children found for %d." %v
	return children

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

def allCyclesMethodRandomized(fracVert=1.0, maxCycles=20):
	cycles = defaultdict(list)
	numFound = Counter()
	for vertex in xrange(vertices):
		if numFound[vertex] >= maxCycles:
			continue
		curr_path = [vertex]
		vert_children = get_children(vertex)
		childrenToConsider = int(ceil(fracVert*len(vert_children)))
		random.shuffle(vert_children)
		for child in vert_children[:childrenToConsider]:
			exploreRandom(child, curr_path, cycles, maxCycles, fracVert, numFound)
	print cycles
	return cycles

def exploreRandom(vertex, curr_path, cycles, maxCycles, fracVert, numFound):
	if vertex == curr_path[0]:
		tmp = rotate_lowest(curr_path)
		if tmp not in cycles[tmp[0]]:
			cycles[tmp[0]].append(tmp)
		numFound[curr_path[0]] += 1
		return
	if numFound[curr_path[0]] >= maxCycles:
		return
	if vertex in curr_path:
		halfpath = curr_path[curr_path.index(vertex):]
		tmp = rotate_lowest(halfpath)
		if tmp not in cycles[tmp[0]]:
			cycles[tmp[0]].append(tmp)
	if numFound[vertex] >= maxCycles:
		return
	curr_path.append(vertex)
	vert_children = get_children(vertex)
	childrenToConsider = int(ceil(fracVert*len(vert_children)))
	random.shuffle(vert_children)
	for child in vert_children[:childrenToConsider]:
		if len(curr_path) == 5 and child != curr_path[0]:
			continue
		exploreRandom(child, curr_path, cycles, maxCycles, fracVert, numFound)
	curr_path.pop()

### UPDATED RANDOMIZED BFS ######

def allCyclesMethodRandomizedBFS(fracVert=0.15, maxCycles=20):
	cycles = defaultdict(list)
	numFound = Counter()
	visited = set()

	for vertex in xrange(vertices):
		if vertex in visited:
			continue
		# to limit search space
		if numFound[vertex] >= maxCycles:
			continue
		exploreRandomBFS(vertex, cycles, maxCycles, fracVert, numFound, visited)
	
	print cycles
	return cycles, visited

def exploreRandomBFS(vertex, cycles, maxCycles, fracVert, numFound, visited):
	toVisit = []

	vert_children = get_children(vertex)
	inds = range(len(vert_children))
	childrenToConsider = int(ceil(fracVert*len(vert_children)))
	random.shuffle(inds)
	for ind in inds[:childrenToConsider]: # visited?
		if vert_children[ind] not in visited:
			toVisit.append((vert_children[ind], [vertex]))

	visited.add(vertex)

	while toVisit:
		curr_Vert, CP = toVisit.pop(0)
		assert originalMatrix[CP[-1]][curr_Vert] == 1
		CP.append(curr_Vert)

		vert_children = get_children(curr_Vert)
		inds = range(len(vert_children))
		childrenToConsider = int(ceil(fracVert*len(vert_children)))
		random.shuffle(inds)
		for ind in inds[:childrenToConsider]:
			child = vert_children[ind]
			if len(CP) < 5 and child not in CP and child not in visited: # visited?
				toVisit.append((child, CP[:]))
				# print 'after update to visit {0}'.format(toVisit)
			elif len(CP) <= 5 and child in CP: # visited?
				path = CP[CP.index(child):]
				# print 'path {0}'.format(path)
				tmp = rotate_lowest(path)
				if tmp not in cycles[tmp[0]]:
					# print 'adding path'
					cycles[tmp[0]].append(tmp)
				# keep track of number of cycles found for this starting vertex
				if child == CP[0]:
					numFound[CP[0]] += 1

		visited.add(curr_Vert)



### UPDATED BFS COMPLETE ######

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
# solution = allCyclesMethodRandomized()
solution, visited = allCyclesMethodRandomizedBFS()

print 'visited {0}'.format(len(visited))

total = 0
vertscovered = set()
for key in solution.keys():
	total += len(solution[key])
	for cycle in solution[key]:
		vertscovered.update(cycle)

def calculateCost(cycle):
	cost = 0
	global kids	
	for elem in cycle:
		if elem in kids:
			cost += 2
		else:
			cost += 1
	return cost

all_cycles = []
for key in solution.keys():
	for cycle in solution[key]:
		all_cycles.append((cycle, calculateCost(cycle)))
	
print "Solution is: ", solution
print 'Number of cycles found: {0}'.format(total)
print "Total vertices covered: ", len(vertscovered), "/ %d" %vertices

##### LP SOLVER ######
import numpy as np
import pulp

def cycleCost(cycle):
    """Calculate the cost of a particular cycle"""
    return cycle[1]

def lpsetpack(cycle_cost_pairs):
	"""Expects a list of ([cycle], cost) tuple pairs."""
	# convert lists to tuples
	cycle_cost_pairs = [(tuple(elem[0]),elem[1]) for elem in cycle_cost_pairs]

	# extract cycles and costs from the given information
    	cycles, costs = zip(*cycle_cost_pairs)

    	# create a set of all individuals
    	patients = set()
    	[patients.update(cycle) for cycle in cycles]

    	x = pulp.LpVariable.dicts('surgery_group', cycle_cost_pairs,
        	                      lowBound = 0,
                	              upBound = 1,
                        	      cat = pulp.LpInteger)

    	#create a binary variable to state that a table setting is used
    	surgery_model = pulp.LpProblem("Kidney Donor/Patient Model", pulp.LpMaximize)

    	# objective function
    	surgery_model += sum([cycleCost(cycle) * x[cycle] for cycle in cycle_cost_pairs])

    	# constraint that patient must appear no more than once
    	for patient in patients:
        	surgery_model += sum([x[cycle] for cycle in cycle_cost_pairs
        	                            if patient in cycle[0]]) <= 1

	# solve the linear program
    	surgery_model.solve()

    	cycles_selected = []
    	for cycle in cycle_cost_pairs:
        	if x[cycle].value() == 1.0:
			print(cycle[0])
			cycles_selected.append(list(cycle[0]))

    	return cycles_selected


finalsol = lpsetpack(all_cycles)
print finalsol

checkValid(finalsol)

#allCyclesMethod()
# 344 352 369 409 413 418 429 and 452 
