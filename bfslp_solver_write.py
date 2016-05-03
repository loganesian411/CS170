# bfs/lp merge
import random
from copy import copy, deepcopy
from collections import defaultdict
from math import ceil
from collections import Counter
import numpy as np
import pulp

##### HELPER FUNCTIONS #####

fracVert = 0.25
maxCycles = 10000000000

def checkValid(soln):
	for item in soln:
		for i in xrange(len(item)):
			if i == len(item)-1:
				if originalMatrix[item[i]][item[0]] != 1:
					print "error2: ", item
			else:
				if originalMatrix[item[i]][item[i+1]] != 1:
					print "error1: ", item

def calculateCost(cycle):
	cost = 0
	global kids	
	for elem in cycle:
		if elem in kids:
			cost += 2
		else:
			cost += 1
	return cost

def get_children(v):
	children = []
	for child in xrange(vertices):
		if matrix[v][child] == 1: 
			children.append(child)
	#print "Children found for %d." %v
	return children

def rotate_lowest(l):
        lowestind = l.index(min(l))
        l = l[lowestind:]+l[:lowestind]
        return l

##### BFS SEARCH #####

def allCyclesMethodRandomizedBFS(fracVert=0.25, maxCycles=20):
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
	
	# print cycles
	print 'found all cycles'
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
			elif len(CP) <= 5 and child in CP: # visited?
				path = CP[CP.index(child):]
				tmp = rotate_lowest(path)
				if tmp not in cycles[tmp[0]]:
					cycles[tmp[0]].append(tmp)
				# keep track of number of cycles found for this starting vertex
				if child == CP[0]:
					numFound[CP[0]] += 1

		visited.add(curr_Vert)

#### LP SOLVER AND HELPER FUNCTION #####

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
			# print(cycle[0])
			cycles_selected.append(list(cycle[0]))

    	return cycles_selected


##### LOAD INSTANCE #####
for i in range(237,238):
    outwriter = open("solutionsLP._238txt", "a")
    outTotals = open("totalsLP_238.txt", "a")
    outCheck = open("checkerLP_238.txt", "a")
    current = i+1
    source_file = "phase1-processed/%d.in" % current
    # source_file = "phase1-processed/10.in"
    # source_file = "phase1-processed/112.in"
    # source_file = "phase1-processed/102.in"
    # source_file = 'phase1-processed/119.in'

    print("Starting file: " + source_file)
    instance = open(source_file, "r")

    vertices = int(instance.readline())
    childLine = instance.readline()
    kids = []
    if childLine not in ('\n', '\r\n'):
        kids = map(int, childLine.strip().split(" "))

    # kids = []
    # kids = map(int, instance.readline().strip().split(" "))
    matrix = [[0 for i in xrange(vertices)] for i in xrange(vertices)]

    for i in xrange(vertices):
        matrix[i] = map(int, instance.readline().strip().split(" "))
    originalMatrix = deepcopy(matrix)

    #### SOLVING #####
    solution, visited = allCyclesMethodRandomizedBFS(fracVert=fracVert, maxCycles=maxCycles)

    total = 0
    for key in solution.keys():
    	total += len(solution[key])

    print 'Number of cycles found: {0}'.format(total)
    print 'Total vertices visited {0}'.format(len(visited))


    #### FORMATTING FOR LP SOLVER #####
    all_cycles = []
    for key in solution.keys():
    	for cycle in solution[key]:
    		all_cycles.append((cycle, calculateCost(cycle)))

    MAXCYCLECT = 6000

    random.shuffle(all_cycles)
    cycles_to_use = all_cycles[:MAXCYCLECT]

    #### LP SOLVE #####
    print "Running LP"
    if cycles_to_use:
        finalsol = lpsetpack(cycles_to_use)
    else:
        finalsol = []
    print "Found solution"

    # OUTPUT IS A LIST OF LISTS
    score = 0
    for item in finalsol:
        score += calculateCost(item)
        printline = ""
    if finalsol:
        for item in finalsol:
            printline += str(item).replace(",","").replace("[","").replace("]","") + "; "
    else:
        printline = "None  "
    printline = printline[:-2]
    outwriter.write(printline + "\n")
    outCheck.write("(Instance %d) " %current + str(printline) + "\n")
    outTotals.write("Instance %d: %d" %(current, score) + "\n")
    #### CHECKING VALIDITY OF SOLUTION #####
    if checkValid(finalsol) == False:
        print "Broke at " + str(i)
        break
    outwriter.close()
    outCheck.close()
    outTotals.close()

