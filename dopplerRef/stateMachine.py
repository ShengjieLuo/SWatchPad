import math


def SMAngle(x1,y1,x2,y2):
	if x1!=x2 and y2>y1:
		angle1 = math.atan((y2-y1)/(x2-x1)) / math.pi * 180	
	elif x1!=x2 and y2<y1:
		angle1 = math.atan((y2-y1)/(x2-x1)) / math.pi * 180 + 360
	elif x2>x1 and y2==y1:
		angle1 = 0.0
	elif x2<x1 and y2==y1:
		angle1 = 180
	elif x1==x2 and y2>y1:
		angle1 = 90.0
	elif x1==x2 and y2<y1:
		angle1 = 270.0
	elif x1==x2 and y1==y2:
		angle1 = -1
	return angle1	


def SMCorrection2D(point,thresold):
	num = len(point)
	state = 0
	resultState = []
	tempState = []
	angleList = []	

	for i in range(1,num-1):
		[x1,y1] = point[i-1]
		[x2,y2] = point[i]
		[x3,y3] = point[i+1]
		angle1 = SMAngle(x1,y1,x2,y2)
		angle2 = SMAngle(x2,y2,x3,y3)
		if angle1 == -1 or angle2 == -1:
			angle = -1
		else:		
			angle = abs(angle2-angle1)
		angleList.append(angle)
	'''
	for i in range(num-2):
		if state == 0 and angle<=90:
			resultState.append([x3,y3])
		elif state == 0 and angle>90:
			state = 1
			resultState.append([x3,y3])
		elif state == 1 and 
		if angle1 == -1:
			result.append([x3,y3])
		elif angle2 == -1
	'''

def SMCorrection(point,thresold):
	num = len(point)
	state = 0
	resultState = [point[0]]
	tempState = []
	for i in range(1,num):
		if state == 0 and point[i][0] == point[i-1][0]:
			resultState.append(point[i])
		elif state == 0 and point[i][0] != point[i-1][0]:
			tempState.append(point[i])
			state = 1
		elif state == 1 and point[i][0] == tempState[-1][0]:
			resultState.append(tempState[-1])
			resultState.append(point[i])
			state = 0
		elif state == 1 and point[i][0] != tempState[-1][0]:
			resultState.append([resultState[-1][0],tempState[-1][1]])	
			tempState = []
			tempState.append(point[i])
	return resultState 
			 
def SMRecord(point,outfile):
	fp = open(outfile,'w')
	for i in range(len(point)):
		string = str(i) + ',' + str(point[i][0]) + ',' + str(point[i][1]) + '\n'
		fp.write(string)
	fp.close()
