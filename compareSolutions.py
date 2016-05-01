reader0 = open("totals.txt", "r")
reader1 = open("totals2.txt", "r")
readersol0 = open("soln.txt")
readersol1 = open("soln2.txt")
writer = open("solutions.out", "w")

for i in xrange(492):
	line0 = reader0.readline().replace(",", "")
	score0 = int(line0.split(" ")[10])
	line1 = reader1.readline().replace(",","")
	score1 = int(line1.split(" ")[10])
	sol0 = readersol0.readline()
	sol1 = readersol1.readline()

	if score0 > score1:
		writer.write(sol0)
		print "Solution 0 wins with score %d over score %d" %(score0, score1)
	else:
		writer.write(sol1)
		print "Solution 1 wins with score %d over score %d" %(score1, score0)

writer.close()
reader0.close()
reader1.close()