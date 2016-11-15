import math

def xydistance(l1,l2,d1,d2):
	x = math.sqrt((d1**2-l1**2)*(d2**2-l2**2)*((l1+l2)**2-(d1-d2)**2))/(2*(d1*l2+d2*l1))
	y = (d2*l1**2 - d1*l2**2 - d1**2*d2 + d2**2*d1)/(2*(d1*l2+d2*l1))
	return x,y


def testdistance(x,y,l1,l2):
	d1 = math.sqrt(x**2+y**2)+math.sqrt(x**2+(l1-y)**2)
	d2 = math.sqrt(x**2+y**2)+math.sqrt(x**2+(l2+y)**2)
	return d1,d2

if __name__=="__main__":
	d1 , d2 = testdistance(5.8,-5.7,2.10,11.95)
	print xydistance(2.10,11.95,d1,d2)

