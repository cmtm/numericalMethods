from Polynomial import Polynomial

def interpolateLagrange(points):
	runningSum = Polynomial([0.0])
	for j in range(len(points)):
		
		runningProduct = Polynomial([1])
		for k in range(len(points)):
			if k != j:
				scale = points[j][0] - points[k][0]
				runningProduct *= Polynomial([-points[k][0]/scale, 1/scale])
		
		runningSum += runningProduct.scale(points[j][1])
	
	return runningSum

print(interpolateLagrange([[0.0,1.2], [1.0, 2.4], [2.0, 3.6], [3.0, 4.8], [4.0, 6.0]]))

HvB = [[0.0, 0.0],[0.2, 14.7],[0.4,36.5],[0.6,71.7],[0.8,121.4],[1,197.4],[1.1,256.2],[1.2,348.7],[1.3,540.6],[1.4,1062.8],[1.5,2318.0],[1.6,4781.9],[1.7,8687.4],[1.8,13924.3],[1.9,22650.2]]
a = interpolateLagrange(HvB[:6])
print([HvB[0],HvB[8],HvB[9],HvB[12],HvB[13],HvB[14]])
b = interpolateLagrange([HvB[0],HvB[8],HvB[9],HvB[12],HvB[13],HvB[14]])