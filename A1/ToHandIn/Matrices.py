import math

class Matrix:
	"""Matrix that has various matrix operations. Defaults to 2x2 identity matrix."""
	
	def __init__(self, numRows=2, numColumns=2, numbers=None):
		self.matrix = None # I just like to declare fields at begining
		self.numRows = numRows
		self.numColumns = numColumns
		
		# make identity matrix if no values are supplied
		if numbers == None:
			self.matrix = [[1 if x == y else 0 for x in range(numColumns)] for y in range(numRows)]
		else:
			#duplicate the matrix to break outside references
			self.matrix = [row[:] for row in numbers]
			self.checkSizeLegal()
	
	def checkSizeLegal(self):
		if len(self.matrix) != self.numRows:
			raise NameError("Incorrect number of rows. Should be {} but is {}.".format(self.numRows, len(self.matrix)))		
		for i in range(self.numRows):
			if len(self.matrix[i]) != self.numColumns:
				raise NameError("Incorrect number of elements in row {}".format(i+1))

	def getValue(self, row, column):
		return self.matrix[row-1][column-1]
		
	def setValue(self, row, column, value):
		self.matrix[row-1][column-1] = value
	
	def multiplyByMatrix(self, rightMatrix):
		if self.numColumns != rightMatrix.numRows:
			raise NameError("Matrix sizes aren't compatible for multiplication.")
		tRight = rightMatrix.getTranspose()
		result = [[ sum( x*y for (x,y) in zip(self.matrix[j], tRight.matrix[i])) \
		                for i in range(rightMatrix.numColumns)] \
		                      for j in range(self.numRows)]
		
		return Matrix(self.numRows, rightMatrix.numColumns, result)
		
	def getTranspose(self):
		return Matrix(self.numColumns, self.numRows, [list(i) for i in zip(*self.matrix)])
	
	def getRawDataRef(self):
		return self.matrix
		
	def printMatrix(self):
		for row in self.matrix:
				for num in row:
					print("{:10.4f}".format(num).rjust(8), end = ' ')
				print()
		
		
class BehavingMatrix(Matrix):
	"""A matrix that is real, symmetric and positive definite"""
	
	def __init__(self, numRows=2, numColumns=2, numbers=None):
		super().__init__(numRows, numColumns, numbers)
		self.n = numRows
		# I might move this check to checkSizeLegal
		if self.numRows != self.numColumns:
			raise NameError("The matrix isn't square.")
		
	"""		
	# override checkSizeLegal to ensure that it's square
	def checkSizeLegal(self):
		# call base-class method
		super().checkSizeLegal()
		# then do specific testing
		if self.numRows != self.numColumns:
			raise NameError("The matrix isn't square.")
		# won't check any of the other conditions
	"""	
	
	# no look-ahead or any other optimization
	def computeLMatrix(self):
		L = Matrix(self.n, self.n) # numRows and numColumns should will be equal
		for j in range(1, self.n + 1):
		
			# sum of row j of L squared
			rowSquared = sum([x*x for x in L.matrix[j-1][:j-1]])
				
			L.setValue(j, j, math.sqrt(self.getValue(j, j) - rowSquared))
			for i in range(j+1, self.n+1):
				dotProduct = sum([L.getValue(i,k) * L.getValue(j,k) for k in range(1,j)])
				
				L.setValue(i, j, (self.getValue(i, j) - dotProduct) / L.getValue(j,j))
		
		return L
	
	def solveSystem(self, b):
		# takes b as a 1D vector
		if len(b) != self.n:
			raise NameError("Length of b not equal to matrix size.")
		L = self.computeLMatrix()
		y = []
		for i in range (1, self.n+1):
			sum = 0
			for j in range(1, i):
				sum += L.getValue(i, j) * y[j-1]
			y.append((b[i-1] - sum) / L.getValue(i, i))
		
		x = []
		for i in range (self.n, 0, -1):
			sum = 0
			for j in range(i+1, self.n+1):
				sum += L.getValue(j, i) * x[-self.n + j-1] # have to go from back
			x.insert(0, (y[i-1] - sum) / L.getValue(i, i))
		
		return x

class BehavingSparseMatrix(BehavingMatrix):
	
	def solveSystem(self, b):
		# takes b as a 1D vector
		if len(b) != self.n:
			raise NameError("Length of b not equal to matrix size.")
		(L, firstNonZero, halfBandwidth) = self.computeLMatrix()
		y = []
		for i in range (1, self.n+1):
			sum = 0
			for j in range(firstNonZero[i-1] + 1, i):
				sum += L.getValue(i, j) * y[j-1]
			y.append((b[i-1] - sum) / L.getValue(i, i))
		
		x = []
		for i in range (self.n, 0, -1):
			sum = 0
			for j in range(i+1, self.n+1):
				sum += L.getValue(j, i) * x[-self.n + j-1] # have to go from back
			x.insert(0, (y[i-1] - sum) / L.getValue(i, i))
		
		return (x, halfBandwidth)
	def computeLMatrix(self):
		# find left-boundaries of A along with half-bandwidth
		# this works in base 0 and NOT matrix base
		firstNonZero = []
		halfBandwidth = 0
		for (j, row) in enumerate(self.matrix):
			for (i, num) in enumerate(row):
				if num != 0:
					firstNonZero.append(i)
					if j - i > halfBandwidth: 
						halfBandwidth = j - i
					break
			else:
				raise NameError("All zero row.")
			
		
		L = Matrix(self.n, self.n) # numRows and numColumns should will be equal
		for j in range(1, self.n + 1):
		
			# sum of row j of L squared
			rowSquared = sum([x*x for x in L.matrix[j-1][firstNonZero[j-1]:j-1]])
				
			L.setValue(j, j, math.sqrt(self.getValue(j, j) - rowSquared))
			for i in range(j+1, self.n+1):
				dotProduct = sum([L.getValue(i,k) * L.getValue(j,k) for k in range(max(firstNonZero[i-1], firstNonZero[j-1]),j)])
				
				L.setValue(i, j, (self.getValue(i, j) - dotProduct) / L.getValue(j,j))
		
		return (L, firstNonZero, halfBandwidth)