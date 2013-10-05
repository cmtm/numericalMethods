import math

def integrate(f, a, b, n):
	segLen = (b-a)/n
	runningSum = 0
	for i in range(n):
		runningSum += f(segLen*(i+0.5))
	return runningSum * segLen

def integrateUneven(f, a, b, relativeWidths):
	scale = (b-a) / sum(relativeWidths)
	widths = [width * scale for width in relativeWidths]
	
	runningWidth = 0
	runningSum = 0
	for w in widths:
		runningSum += f(w/2 + runningWidth) * w
		runningWidth += w
	
	return runningSum
print('------------------------------')
error = ["[{}, {}]".format(i, abs(math.sin(1) - integrate(math.cos, 0.0, 1.0, i))) for i in range(1, 20 + 1)]
print("[{}]".format(",".join(error)))

print('------------------------------')
error = ["[{}, {}]".format(i, abs(-1 - integrate(math.log, 0.0, 1.0, i))) for i in range(10, 201, 10)]
print("[{}]".format(",".join(error)))

print('------------------------------')
result = integrateUneven(math.log, 0.0, 1.0, [1,2,4,8,16,32,64,128,256, 512])
print("{:>3} {:<10.6}".format(10, abs(-1-result)))

"""
print('------------------------------')
for i in range(1, 20 + 1):
	result = integrate(math.cos, 0.0, 1.0, i)
	print("{:>3} {:<10.6}".format(i, abs(math.sin(1) - result)))

print('------------------------------')
for i in range(10, 201, 10):
	result = integrate(math.log, 0.0, 1.0, i)
	print("{:>3} {:<10.6}".format(i, abs(-1 - result)))

print('------------------------------')
result = integrateUneven(math.log, 0.0, 1.0, [1,2,4,8,16,32,64,128,256, 512])
print("{:>3} {:<10.6}".format(10, abs(-1-result)))
"""