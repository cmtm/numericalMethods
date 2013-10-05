from Polynomial import Polynomial

p1 = Polynomial([2.4,3.2,4.0])
p2 = Polynomial([0.0, 3.2, 1.1, 5.5, 2.0, 0.0])

print(p1)
print(p2)

p3 = p1 + p2
print(p3)

p4 = p3 * p1
print(p4)

p5 = p4.scale(1/51)
print(p5)