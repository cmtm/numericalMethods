class Item():
	# static variables
	nodesCreated = 0
	branchesCreated = 0
	
	# Enum
	Node = 0
	Branch = 1
	Empty = 2
	
	def __init__(self, type):
		self.type = type
		if type == Item.Node:
			self.itemNum = Item.nodesCreated
			Item.nodesCreated += 1
		elif type == Item.Branch:
			self.itemNum = Item.branchesCreated
			Item.branchesCreated += 1
	def reset():
		Item.nodesCreated = 0
		Item.branchesCreated = 0
		
class Branch():
	# static variable
	branchesCreated = 0
	
	def __init__(self):
		self.branchNum = self.branchesCreated
		self.branchesCreated += 1


def generateEvenRow(N):
	return [Item(Item.Node) if x%2 == 0 else Item(Item.Branch) for x in range(4*N - 1)]

def generateOddRow(N):
	return [Item(Item.Branch) if x%2 == 0 else Item(Item.Empty) for x in range(4*N - 1)]

def generateNetworkFile(fileOut, N):
	Item.reset() # reset item counts
	# generate test branch
	Item(Item.Branch)
	
	mesh = [generateEvenRow(N) if x%2 == 0 else generateOddRow(N) for x in range(2*N - 1)]
	
	branchValues = []
	nodeEquations = []
	# this little block allows us to visualize the mesh
	visualMesh = [['n' if item.type == Item.Node \
	                  else ('b' if item.type == Item.Branch else ' ') \
	                       for item in row] for row in mesh]
	for row in visualMesh:
		print(' '.join(row))
	numBranches = 1
	# all current goes down-right
	for y in range(len(mesh)):
		for x in range(len(mesh[0])):
			# case of node: create incidence matrix row
			# first node is ground
			if mesh[y][x].type == Item.Node and ( x != 0 or y != 0):
				branches = []
				# check all around
				if x > 0:
					branches.append((mesh[y][x-1].itemNum, -1))
				if y > 0:
					branches.append((mesh[y-1][x].itemNum, -1))
				if x < len(mesh[0]) - 1:
					branches.append((mesh[y][x+1].itemNum, 1))
				if y < len(mesh) - 1:
					branches.append((mesh[y+1][x].itemNum, 1))
				# this last branch is the test source resistance
				if y == len(mesh) - 1 and x == len(mesh[0]) - 1:
					branches.append((0, 1))
				nodeEquations.append(['1' if (x, 1) in branches else ('-1' if (x, -1) in branches else '0') for x in range(4 * N*N - 3*N + 1)])
			# I'm counting branches just as a sanity check, there should be 4*N*N - 3*N + 1 of them
			if mesh[y][x].type == Item.Branch:
				numBranches += 1
	
	# sanity check
	if Item.branchesCreated != 4*N*N - 3*N + 1:
		raise NameError("There aren't 4*N*N - 3*N branches, there are {}".format(numBranches))
	fileOut.write("{}\n\n".format(Item.branchesCreated))
	for b in range(Item.branchesCreated):
		if b == 0:
			fileOut.write("0 1 -1\n")
		else:
			fileOut.write("0 1 0\n")
	fileOut.write('\n')
	for eq in nodeEquations:
		fileOut.write("{}\n".format(' '.join(eq)))

for N in range(2, 11):
	fileOut = open('output{}.txt'.format(N), 'w')
	generateNetworkFile(fileOut, N)
	fileOut.close()
