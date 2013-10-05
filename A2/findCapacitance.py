nodesWide = 6
nodesHigh = 6

mesh = [[None for x in range(nodesWide)] for y in range(nodesHigh)]

# read mesh values
for line in open('simple2Dresults.txt', 'r'):
	splitLine = line.strip().split()
	if len(splitLine) > 0 and splitLine[0].isdigit():
		xNode = int(float(splitLine[1]) / 0.02)
		yNode = int(float(splitLine[2]) / 0.02)
		mesh[yNode][xNode] = float(splitLine[3])
	
# voltage is 10 volts on inner conductor
mesh[0][0] = 10.0
mesh[0][1] = 10.0

# compute individual energies and add them all up by using
# the equations devellopped in part a and by expanding on
# them, we were able to find the energy in a square when
# the potential at the corners is known. Assuming u1, u2, u3, u4
# to the the potentials at the corners of the square in the
# assignment handout, the energy is equal to 1/2 * epsilon *
# u1^2 - u1*u2 - u1*u4 + u2^2 - u2*u3 + u3^2 - u3*u4 + u4^2

totalEnergy = 0.0
for y in range(nodesHigh - 1):
	for x in range(nodesWide - 1):
		u1 = mesh[y+1][x]
		u2 = mesh[y][x]
		u3 = mesh[y][x+1]
		u4 = mesh[y+1][x+1]
		
		totalEnergy += u1*u1 - u1*u2
		totalEnergy += -u1*u4 + u2*u2
		totalEnergy += -u2*u3 + u3*u3
		totalEnergy += -u3*u4 + u4*u4
		
epsilon = 8.854187817620e-12
voltageSquared = 100
totalEnergy *= epsilon * 4 / voltageSquared

print(totalEnergy)