import math

class StrongFiniteDiffSolver():
	
	def __init__(self,horizontalLines, verticalLines):
		self.CABLE_HEIGHT = 0.1
		self.CABLE_WIDTH = 0.1
		self.CORE_HEIGHT = 0.02
		self.CORE_WIDTH = 0.04
		self.CORE_POTENTIAL = 10
		self.MIN_RESIDUAL = 0.0001
		
		self.horizontalLines = horizontalLines
		self.verticalLines = verticalLines
		
		self.mesh = self.generateInitialMesh()
		
	def generateInitialMesh(self):
		# create mesh and set dirchlet boundary values
		mesh = [[10.0 if x <= self.CORE_WIDTH and y <= self.CORE_HEIGHT else 0.0 \
		          for x in self.verticalLines] \
				  for y in self.horizontalLines]
		# set neumann boundary values
		rateOfChange = -10/(self.CABLE_HEIGHT - self.CORE_HEIGHT)
		for y in range(len(self.horizontalLines)):
			if self.horizontalLines[y] > self.CORE_HEIGHT:
				mesh[y][0] = 10 + rateOfChange * (self.horizontalLines[y] - self.CORE_HEIGHT)
		
		rateOfChange = -10/(self.CABLE_WIDTH - self.CORE_WIDTH)
		for x in range(len(self.verticalLines)):
			if self.verticalLines[x] > self.CORE_WIDTH:
				mesh[0][x] = 10 + rateOfChange * (self.verticalLines[x] - self.CORE_WIDTH)

		return mesh

	def solveWithSOR(self, w):
		iterations = 0
		while self.computeMaxResidual() > self.MIN_RESIDUAL:
			self.iterateSOR(w)
			iterations += 1
		return iterations
	
	def getComputedPotential(self, x, y):
		# just a floor, not a round or linear interpolation
		xNode = self.verticalLines.index(x)
		yNode = self.horizontalLines.index(y)
		return self.mesh[yNode][xNode]
		
	def iterateSOR(self, w):	
		for y in range(1, len(self.horizontalLines)-1):
			for x in range(1, len(self.verticalLines)-1):
				if self.verticalLines[x] > self.CORE_WIDTH or self.horizontalLines[y] > self.CORE_HEIGHT:
					d1 = self.verticalLines[x] - self.verticalLines[x-1]
					d2 = self.horizontalLines[y+1] - self.horizontalLines[y]
					d3 = self.verticalLines[x+1] - self.verticalLines[x]
					d4 = self.horizontalLines[y] - self.horizontalLines[y-1]

					self.mesh[y][x] = (self.mesh[y][x-1]/(d1*(d1+d3)) \
             		      + self.mesh[y][x+1]/(d3*(d1+d3)) + self.mesh[y-1][x]/(d4*(d2+d4)) + self.mesh[y+1][x]/(d2*(d2+d4))) / (1/(d1*d3) + 1/(d2*d4))
					

	def computeMaxResidual(self):
		maxResidual = 0
		for y in range(1, len(self.horizontalLines) - 1):
			for x in range(1, len(self.verticalLines) - 1):
				if self.horizontalLines[y] > self.CORE_HEIGHT or self.verticalLines[x] > self.CORE_WIDTH:
					d1 = self.verticalLines[x] - self.verticalLines[x-1]
					d2 = self.horizontalLines[y+1] - self.horizontalLines[y]
					d3 = self.verticalLines[x+1] - self.verticalLines[x]
					d4 = self.horizontalLines[y] - self.horizontalLines[y-1]

					residual = (self.mesh[y][x-1]/(d1*(d1+d3)) + self.mesh[y][x+1]/(d3*(d1+d3)) + self.mesh[y-1][x]/(d4*(d2+d4)) + self.mesh[y+1][x]/(d2*(d2+d4))) - (1/(d1*d3) + 1/(d2*d4))*self.mesh[y][x]
					residual = math.fabs(residual)
					if residual > maxResidual:
						maxResidual = residual
		return maxResidual