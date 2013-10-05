HvB = [[0.0, 0.0],[0.2, 14.7],[0.4,36.5],[0.6,71.7],[0.8,121.4],[1,197.4],[1.1,256.2],[1.2,348.7],[1.3,540.6],[1.4,1062.8],[1.5,2318.0],[1.6,4781.9],[1.7,8687.4],[1.8,13924.3],[1.9,22650.2]]

def Hvalue(flux):
	B = flux/(1/pow(100,2))
	# interpolate for values outside domain
	if B > HvB[-1][0]:
		slope = (HvB[-1][1] - HvB[-2][1]) / (HvB[-1][0] - HvB[-2][0])
		return (B - HvB[-1][0]) * slope + HvB[-1][1]
	
	for i in range(len(HvB)):
		if HvB[i][0] > B:
			slope = (HvB[i][1] - HvB[i-1][1]) / (HvB[i][0] - HvB[i-1][0])
			return (B - HvB[i-1][0]) * slope + HvB[i-1][1]
	else: # must be smaller
		slope = (HvB[1][1] - HvB[0][1]) / (HvB[1][0] - HvB[0][0])
		return (B - HvB[0][0]) * slope + HvB[0][1]
	

def Hderivative(flux):
	B = flux/(1/pow(100,2))
	if B > HvB[-1][0]:
		return (HvB[-1][1] - HvB[-2][1]) / (HvB[-1][0] - HvB[-2][0])
	
	for i in range(len(HvB)):
		if HvB[i][0] > B:
			slope = (HvB[i][1] - HvB[i-1][1]) / (HvB[i][0] - HvB[i-1][0])
			return slope
	else: # must be smaller
		slope = (HvB[1][1] - HvB[0][1]) / (HvB[1][0] - HvB[0][0])
		return slope
		
def fNewton(flux):
	return 39.78873577e6 * flux + 0.3*Hvalue(flux) - 8e3
	
def fderivative(flux):
	return 39.78873577e6 + 0.3*Hderivative(flux)/(1/pow(100,2))

def fSubstitution(flux):
	return 8000/(39.78873577e6 + 0.3*Hvalue(flux)/flux)

def fSubstitution2(flux):
	return (8000-0.3*Hvalue(flux)) / 39.78873577e6
	
def newtonRaph(x, tolerance):
	i = 0
	while abs(fNewton(x)/fNewton(0)) > tolerance:
		i += 1
		x -= fNewton(x)/fderivative(x)
	
	print("Flux of {} acheived after {} iterations.".format(x, i))
	return x

def successiveSub(x, tolerance):
	i = 0
	while abs(fNewton(x)/fNewton(0)) > tolerance:
		i += 1
		x = fSubstitution(x) 
		print(x)
	
	print("Flux of {} acheived after {} iterations.".format(x, i))
	return x

def successiveSub2(x, tolerance):
	i = 0
	while abs(fNewton(x)/fNewton(0)) > tolerance:
		i += 1
		x = fSubstitution2(x) 
		print(x)
	
	print("Flux of {} acheived after {} iterations.".format(x, i))
	return x
	
newtonRaph(0, 1e-6)
print('-----------------------')
points = ["[{},{}]".format((i+1)/1e6, fSubstitution((i+1)/1e6)) for i in range(300)]
print("[{}]".format(",".join(points)))
print('-----------------------')
successiveSub(1e-6, 1e-6)