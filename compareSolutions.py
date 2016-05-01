reader0 = open("soln.txt", "r")
reader1 = open("soln1.txt", "r")
writer = open("solutions.out", "w")

for i in xrange(492):
	line0 = reader0.readline()
	score0 = line0.split(" ")[10]
	line1 = reader1.readline()
	score1 = line1.split(" ")[10]

	if score0 > score1:
		writer.write(line0)
		print "Solution 0 wins with score %d over score %d" %(score0, score1)
	else:
		writer.write(line1)
		print "Solution 1 wins with score %d over score %d" %(score1, score0)

writer.close()
reader0.close()
reader1.close()