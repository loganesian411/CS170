import random
from copy import copy, deepcopy


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

def greedyExplore(s, start_path, cycles):
	#print "starting explore for current path " + str(curr_path) + " and vertex %d" %vertex
	stack = [(s, start_path)]
	while stack:
		vertex, curr_path = stack.pop()
		if len(curr_path) > 5:
			continue
		if len(curr_path) != 0:
			if vertex == curr_path[0]:
				curr_path = rotate_lowest(curr_path)
				if curr_path not in cycles:
					cycles.append(curr_path)
				break
			if vertex in curr_path:
				curr_path2 = rotate_lowest(curr_path[index(vertex):])
				if curr_path2 not in cycles:
					cycles.append()
				continue
		children = get_children(vertex)
		curr_path2 = curr_path[:]
		curr_path2.append(vertex)
		for child in children:
			#print "finding children of vertex:", vertex, child
			stack.append((child, curr_path2))

def greedyMethod():
	print "Starting Greedy Strategy..."
	nodes = set()
	answer = []
	kidDonors = getKids()
	for i in xrange(vertices):
		nodes.add(i)
	while nodes:
		#if kidDonors:
		#	rand = random.randrange(0, len(kidDonors))
		#	currNode = kidDonors.pop(rand)
		#else:
		#	currNode = random.sample(nodes, 1)[0]
		currNode = random.sample(nodes, 1)[0]
		print "Analyzing node %d" %currNode
		print "%d out of %d nodes left." %(len(nodes),vertices)
		cycles = []
		for child in get_children(currNode):
			curr_path = []
			greedyExplore(child, curr_path, cycles)
		print len(cycles), cycles
		cycles = sorted(cycles, key = len)
		if len(cycles) == 0:
			nodes.remove(currNode)
		else:
			bestCycle = cycles[-1]
			for item in bestCycle:
				# if item in kidDonors:
				# 	kidDonors.remove(item)
				nodes.remove(item)
				for i in xrange(vertices):
					matrix[i][item] = 0
			answer.append(bestCycle)
	return answer

outwriter = open("soln.txt", "w")
outTotals = open("totals.txt", "w")
outCheck = open("checker.txt", "w")
for i in xrange(192):
	current = i+301
	source_file = "phase1-processed/%d.in" % current
	#source_file = "phase1-processed/212.in"
	print("Starting file: " + source_file)
	instance = open(source_file, "r")

	vertices = int(instance.readline())
	# kids = instance.readline()
	# kids = []
	kids = map(int, instance.readline().strip().split(" "))
	matrix = [[0 for i in xrange(vertices)] for i in xrange(vertices)]

	for i in xrange(vertices):
		matrix[i] = map(int, instance.readline().strip().split(" "))
	originalMatrix = deepcopy(matrix)

	solution = greedyMethod()
	if checkValid(solution) == False:
		print "Broke at " + str(i)
		break
	total = 0
	for item in solution:
		total += len(item)

	# if total >= vertices*.1:
	print "Solution: ", solution
	totalStr =  "Total vertices covered: %d / %d" %(total, vertices)
	print totalStr
	outTotals.write(totalStr + "\n")
	printline = ""
	for item in solution:
		printline += str(item).replace(",","").replace("[","").replace("]","") + "; "
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

