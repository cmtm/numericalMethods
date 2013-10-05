from itertools import zip_longest

class Polynomial:

	epsilon = 1.0e-10
	def __init__(self, coefficients = [0.0]):
		# remove zeros from beginning
		for i in range(len(coefficients) - 1, -1, -1):
			if coefficients[i] != 0.0:
				self.highestOrder = i
				self.coefficients = coefficients[0:i+1]
				break
		else:
			self.highestOrder = len(coefficients) - 1
			self.coefficients = coefficients
	
	def evalAt(self, x):
		runningSum = 0
		for i in range(len(self.coefficients)):
			runningSum += self.coefficients*pow(x, i)
	
	def scale(self, c):
		newCoefficients = [c*x for x in self.coefficients]
		return self.__class__(newCoefficients) 
	
	def __add__(self, other):		
		return self.__class__(self.listAdd(self.coefficients, other.coefficients))
	
	# slow method
	def __sub__(self, other):
		return self + other.scale(-1.0)
	
	def __mul__(self, other):
		runningSum = [0.0 for i in range(self.highestOrder + other.highestOrder - 1)]
		for i in range(len(other.coefficients)):
			runningSum = self.listAdd(runningSum, [0]*i+[other.coefficients[i]*x for x in self.coefficients])
		return self.__class__(runningSum)
			
	@staticmethod
	def listAdd(a,b):
		zipped = zip_longest(a, b, fillvalue = 0.0)
		return [x+y if abs(x+y) > Polynomial.epsilon else 0.0 for x,y in zipped]
		# return [x+y for x,y in zipped]
	
	def __str__(self):
		l = ["{:.5}x^{}".format(self.coefficients[i], i) for i in range(len(self.coefficients) - 1, -1, -1)]
		return " + ".join(l)
		"""
		for i in range(len(self.coefficients) - 1, -1, -1):
			print("{:.3}x^{}{}".format(self.coefficients[i], i, "" if i == 0 else " + "))
		"""