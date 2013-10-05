#from Matrices import BehavingMatrix
import Matrices
# ----------- Testing --------------
"""
test matrices
A1 was selected as I wanted to make sure the program
could handle the edge case of a 1x1 matrix.
A2, A3 and A5 are standard positive definite matrices. Their
positive definateness was verified with Maple
"""
A1 = Matrices.BehavingMatrix(1,1, [[2]])	
A2 = Matrices.BehavingMatrix(2,2, [[2,-1], [-1, 2]])
A3 = Matrices.BehavingMatrix(3,3, [[25, 15, -5], [15, 18, 0], [-5, 0, 11]])
A5 = Matrices.BehavingMatrix(5,5, [[23,7,-6,-1,6],[7,18,-6,4,3],[-6,-6,9,0,0],[-1,4,0,9,6],[6,3,0,6,10]])
# x1 = [4]             b1 = [8]
# x2 = [-1,7]          b2 = [-5, 13]
# x3 = [1,2,3]         b3 = [40, 51, 28]
# x5 = [-1,-3,2,4,-2]  b5 = [-72, -63, 42, 13, -11]

print(A1.solveSystem([8]))
print(A2.solveSystem([-9,15]))
print(A3.solveSystem([40,51,28]))
print(A5.solveSystem([-72, -63, 42, 13, -11]))