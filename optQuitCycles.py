import random
from copy import copy, deepcopy
import Queue
import time

BRANCHING_FACTOR = 5
removed = set()

def get_children(v):
	global removed
	children = []
	for child in xrange(vertices):
		if child not in removed and matrix[v][child] == 1:
			children.append(child)
	#print "Children found for %d." %v
	return children

def get_some_children(v):
	global removed
	children = []
	for child in xrange(vertices):
		if child not in removed and matrix[v][child] == 1: 
			children.append(child)
	#print "Children found for %d." %v
	global BRANCHING_FACTOR
	if len(children) > BRANCHING_FACTOR:
		return random.sample(children, BRANCHING_FACTOR)
	else:
		return children

def rotate_lowest(l):
	lowest = min(l)
	while l[0] != lowest:
		l = l[-1:] + l[:-1]
	return l

def checkValid(soln):
	for item in soln:
		for i in xrange(len(item)):
			if i == len(item)-1:
				if originalMatrix[item[i]][item[0]] != 1:
					print "error2: ", item
					return False
			else:
				if originalMatrix[item[i]][item[i+1]] != 1:
					print "error1: ", item
					return False

def getKids():
	return kids

def greedyExplore(s, start_path, cycles, t_end):
	#print "starting explore for current path " + str(curr_path) + " and vertex %d" %vertex
	q = Queue.PriorityQueue()
	q.put((0, s, start_path))

	while not q.empty() and len(cycles) == 0:
		length, vertex, curr_path = q.get()
		length = -length
		if length >= 2:
			if vertex == curr_path[0]:
				curr_path = rotate_lowest(curr_path)
				if curr_path not in cycles:
					cycles.append(curr_path)
				break
			if vertex in curr_path:
				continue
		if length == 5:
			continue
		#print("Looking up children for vertex %d" % vertex)
		if time.time() < t_end:
			children = get_children(vertex)

		else:
			children = get_some_children(vertex)
		curr_path2 = curr_path[:]
		curr_path2.append(vertex)
		for child in children:
			#print "finding children of vertex:", vertex, child
			q.put((-length - 1, child, curr_path2))


def findSoln(originalMatrix, vertices):
	global removed
	removed = set()
	matrix = deepcopy(originalMatrix)

	vertexQ = Queue.PriorityQueue()
	for i in xrange(vertices):
		childList = get_children(i)
		vertexQ.put((len(childList), i))

	solution = greedyMethod(vertexQ)
	score = 0
	for cycle in solution:
		for vert in cycle:
			if vert in kids:
				score += 2
			else:
				score += 1

	total = 0
	for item in solution:
		total += len(item)

	return (score, total, solution)

def greedyMethod(vertexQ):
	print "Starting Greedy Strategy..."
	t_end = time.time() + 60 * 1
	global removed
	answer = []
	kidDonors = getKids()
	while not vertexQ.empty():
		#if kidDonors:
		#	rand = random.randrange(0, len(kidDonors))
		#	currNode = kidDonors.pop(rand)
		#else:
		#	currNode = random.sample(nodes, 1)[0]
		numChildren, currNode = vertexQ.get()
		if currNode in removed:
			print "Vertex %d already removed. Moving on..." % currNode
			continue
		print "Analyzing node %d" %currNode
		print "%d out of %d nodes left." %(vertexQ.qsize() + 1, vertices)
		cycles = []
		for child in get_some_children(currNode):
			curr_path = []
			greedyExplore(child, curr_path, cycles, t_end)
		cycles = sorted(cycles, key = len)
		#print "Explore returned ", cycles, " with list length: %d" % len(cycles)
		if len(cycles) == 0:
			removed.add(currNode)
		else:
			bestCycle = cycles[-1]
			for item in bestCycle:
				# if item in kidDonors:
				# 	kidDonors.remove(item)
				removed.add(currNode)
				for i in xrange(vertices):
					matrix[i][item] = 0
			answer.append(bestCycle)
	return answer

outwriter = open("solutions.out", "w")
outTotals = open("totals.out", "w")
outCheck = open("checker.out", "w")
for i in xrange(492):
	current = i+1
	t_start = time.time()
	source_file = "phase1-processed/%d.in" % current
	#source_file = "phase1-processed/212.in"
	print("Starting file: " + source_file)
	instance = open(source_file, "r")

	vertices = int(instance.readline())
	childLine = instance.readline()
	kids = []
	if childLine not in ('\n', '\r\n'):
		kids = map(int, childLine.strip().split(" "))

	removed = set()
	matrix = [[0 for i in xrange(vertices)] for i in xrange(vertices)]

	for i in xrange(vertices):
		matrix[i] = map(int, instance.readline().strip().split(" "))
	originalMatrix = deepcopy(matrix)

	score, total, solution = findSoln(originalMatrix, vertices)

	if time.time() < t_start + 1 and total != vertices:
		for i in xrange(3):
			newscore, newtotal, newsolution = findSoln(originalMatrix, vertices)
			if newscore > score:
				score = newscore
				total = newtotal
				solution = newsolution


	if checkValid(solution) == False:
		print "Broke at " + str(i)
		break


	# if total >= vertices*.1:
	print "Solution: ", solution
	edges = 0
	for row in xrange(len(originalMatrix)):
		for col in xrange(len(originalMatrix[0])):
			edges += originalMatrix[row][col]
	totalStr =  "Total vertices covered: %d / %d for a score of %d, Number of edges: %d" %(total, vertices, score, edges)
	print totalStr
	outTotals.write(totalStr + "\n")
	printline = ""
	if solution:
		for item in solution:
			printline += str(item).replace(",","").replace("[","").replace("]","") + "; "
	else:
		printline = "None  "
	printline = printline[:-2]
	outwriter.write(printline + "\n")
	outCheck.write("(Instance %d) " %current + str(printline) + "\n")
	# else:
	# 	matrix = originalMatrix[:]
	# 	solution = allCyclesMethod()
outwriter.close()

	#print "Solution is: ", solution
outwriter.close()
outCheck.close()
outTotals.close()
	
	#checkValid(solution)
#allCyclesMethod()

