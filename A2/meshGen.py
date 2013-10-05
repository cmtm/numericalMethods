out = open("fileForSimple2D.txt", 'w')

numHorizNodes = 6
numVertiNodes = 5

mesh = [[x + y*numHorizNodes for x in range(1, numHorizNodes + 1)] for y in range(numVertiNodes)]

for y in range(numVertiNodes):
	for x in range(numHorizNodes):
		out.write("{:<3} {:>6} {:>6}\n".format(mesh[y][x], x*0.02, (y+1)*0.02))
out.write("/\n")

# bottom triangles
for y in range(numVertiNodes - 1):
	for x in range(numHorizNodes - 1):
		out.write("{:<3} {:<3} {:<3} {}\n".format(mesh[y][x], mesh[y][x+1], mesh[y+1][x], "0.0000"))

# top triangles
for y in range(1, numVertiNodes):
	for x in range(numHorizNodes - 1):
		out.write("{:<3} {:<3} {:<3} {}\n".format(mesh[y][x], mesh[y-1][x+1], mesh[y][x+1], "0.0000"))
		
out.write("/\n")

for x in range(numHorizNodes):
	out.write("{:<3} {}\n".format(mesh[numVertiNodes-1][x], "0.000"))

for y in range(numVertiNodes - 1):
	out.write("{:<3} {}\n".format(mesh[y][numHorizNodes - 1], "0.000"))
out.close()