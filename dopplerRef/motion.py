from scipy import stats
import math
import pandas as pd

def motionValueTest(Peak,initialFile,thresold):
	# input: peak value, statInfo
	# output: whether it is a singular value
	PeakData = pd.read_csv(initialFile)
	#print "#1 data.describe"
	#print PeakData.describe()
	#print "#2 data.describe"
	PeakData =  PeakData.T
	#print PeakData
	#print "#3 data.test"
	#print PeakData.describe()
	#print "Peak:",Peak
	channel1 = PeakData.ix[:,0]
	channel2 = PeakData.ix[:,1]
	testResult1 = stats.ttest_1samp(a=channel1,popmean=Peak[0])
	testResult2 = stats.ttest_1samp(a=channel2,popmean=Peak[1])
	isValue = []
	print "testResult:",testResult1[1],testResult2[1]
	if testResult1[1]<thresold:
		isValue.append(testResult1[1])
	else:
		isValue.append(-1)
	if testResult2[1]<thresold:
		isValue.append(testResult2[1])
	else:
		isValue.append(-1)
	return isValue


def motionValueVerify(initialFile,channel1,channel2):
	PeakData = pd.read_csv(initialFile)
	PeakData = PeakData.T
	testResult1 = stats.ttest_1samp(a=channel1,popmean=Peak[0])
	testResult2 = stats.ttest_1samp(a=channel2,popmean=Peak[1])
	print "testResult:",testResult1[1],testResult2[1]

'''
#old version in 05.17
def motionEnergyDistance(PeakInfo,StatInfo,initialFile,thresold):
	# input: peak value, statInfo , isValueFlag
	# output: distance of different channel1
	dist = []
	for i in range(len(PeakInfo)):
		[flag1,flag2] = motionValueTest(PeakInfo[i],initialFile,thresold)
		if flag1==1:
			dist1 = StatInfo[0] / PeakInfo[i][0]
		else:
			dist1 = -1
		if flag2==1:
			dist2 = StatInfo[1] / PeakInfo[i][1]
		else:
			dist2 = -1
		dist.append([dist1,dist2])
	return dist
'''

def motionValueTestB(Peak,Stat):
	if Peak[0]> Stat[0]*2/3 and Peak[0] < Stat[0] * 4/3: 	
		flag1 = -1
	else:
		flag1 = 1 #with influence
	if Peak[1]>Stat[1]*2/3 and Peak[1]<Stat[1] * 4/3:
		flag2 = -1
	else:
		flag2 = 1
	return [flag1,flag2]


#version in 05.23
def motionEnergyDistance(PeakInfo,StatInfo,initialFile,thresold):
	# input: peak value, statInfo , isValueFlag
	# output: distance of different channel1
	dist = []
	for i in range(len(PeakInfo)):
		[flag1a,flag2a] = motionValueTest(PeakInfo[i],initialFile,thresold)
		[flag1b,flag2b] = motionValueTestB(PeakInfo[i],StatInfo)
		if flag1a !=-1 and flag1b != -1:
			dist1 = -1*math.log10(flag1a)
		else:
			dist1 = -1
		if flag2a !=-1 and flag2b != -1:
			dist2 = -1*math.log10(flag2a)
		else:
			dist2 = -1
		dist.append([dist1,dist2])
	return dist

def motionFreqDetect(freqInfo):
	#direct = 1 near
	#direct = -1 far
	#direct = 0 ignore
	velocity = []	
	for i in range(len(freqInfo)):
		speed1 =  abs(freqInfo[i][0])
		if freqInfo[i][0] > 2:
			direct1 = 1
		elif freqInfo[i][0] <-2:
			direct1 = -1
		else:
			direct1 = 0
		speed2 = abs(freqInfo[i][1])
		if freqInfo[i][1] > 5:
			direct2 = 1
		elif freqInfo[i][1]<-5:
			direct2 = -1
		else:
			direct2 = 0
		stat = [speed1,speed2,direct1,direct2]
		velocity.append(stat)
	return velocity

'''
#old version in 05.17
def motion2D(dist,velo):
	pointx,pointy = 0,0
	point = []
	for i in range(2,len(dist)):
		if abs(velo[i][0]) >= abs(velo[i][1]) and velo[i][2] != 0:
			pointy = pointy + velo[i][2]*velo[i][0]
		elif abs(velo[i][0]) < abs(velo[i][1]) and velo[i][3] != 0:
			pointy = pointy + velo[i][1]*velo[i][3]
		if dist[i-1][0] == -1 and dist[i][0] >0:
			pointx = pointx - 30
		elif dist[i-1][0] >0 and dist[i][-1] == -1:
			pointx = pointx + 30
		if dist[i-1][1] == -1 and dist[i][-1]>0:
			pointx = pointx + 30
		elif dist[i-1][1] >0 and dist[i][-1] == -1:
			pointx = pointx - 30
		point.append([pointx,pointy])
	return point				
'''

'''
#version in 05.23
def motion2D(dist,velo):
	pointx,pointy = 0,0
	point = []
	for i in range(1,len(dist)):
		if abs(velo[i][0]) >= abs(velo[i][1]) and velo[i][2] != 0:
			pointy = pointy - velo[i][2]*velo[i][0]
		elif abs(velo[i][0]) < abs(velo[i][1]) and velo[i][3] != 0:
			pointy = pointy - velo[i][1]*velo[i][3]
		if (dist[i][0]==-1) and (dist[i][1]==-1):
			#pointx = "NaN"
			pointx = 0
		elif (dist[i][0]!=-1) and (dist[i][1]==-1):
			pointx = -2
		elif (dist[i][0]==-1) and (dist[i][1]!=-1):
			pointx = 2
		elif abs(dist[i][0]-dist[i][1]) <= 3:
			pointx = 0
		elif dist[i][0] > dist[i][1]:
			pointx = -1
		elif dist[i][0] < dist[i][1]:
			pointx = 1
		point.append([pointx,pointy])
	return point				
'''

#version in 05.29
def motion2D(dist,velo):
	pointx,pointy = 0,0
	point = []
	for i in range(1,len(dist)):
		if (dist[i][0]==-1) and (dist[i][1]==-1):
			#pointx = "NaN"
			pointx = 0
		elif (dist[i][0]!=-1) and (dist[i][1]==-1):
			pointx = -2
		elif (dist[i][0]==-1) and (dist[i][1]!=-1):
			pointx = 2
		elif abs(dist[i][0]-dist[i][1]) <= 3:
			pointx = 0
		elif dist[i][0] > dist[i][1]:
			pointx = -1
		if pointx<0 and velo[i][2] != 0:
			pointy = pointy - velo[i][2]*velo[i][0]
		elif pointx>0 and  velo[i][3] != 0:
			pointy = pointy - velo[i][1]*velo[i][3]
		elif pointx==0 and (abs(velo[i][0]) >= abs(velo[i][1])) and velo[i][2] != 0:
			pointy = pointy - velo[i][2]*velo[i][0]
		elif pointy==0 and (abs(velo[i][0]) < abs(velo[i][1])) and velo[i][3] != 0:
			pointy = pointy - velo[i][1]*velo[i][3]
		point.append([pointx,pointy])
	return point				

def motionLoadInit(initialFile):
	fp = open(initialFile)
	line = fp.readlines()[0]
	line = line.split(',')
	line[-1] = line[-1][:-1]
	for i in range(len(line)):
		 line[i] = float(line[i])
	return line


def motionRecord(point,outfile):
	fp = open(outfile,'w')
	for i in range(len(point)):
		string = str(i) + ',' + str(point[i][0]) + ',' + str(point[i][1]) + '\n'
		fp.write(string)
	fp.close()

def motionDetection(AnaResult,initialFile,outfile,thresold):
	# input: peak value
	# output: channel1 distance, channel2 distance
	#print "Analysis result:",AnaResult
	peak = []
	freq = []
	StatInfo = motionLoadInit(initialFile[1])
	for i in range(len(AnaResult)):
		freq.append(AnaResult[i][0:2])
		peak.append(AnaResult[i][2:4])
	#print "peakInfo:",peak
	#print "freqInfo:",freq	
	dist = motionEnergyDistance(peak,StatInfo,initialFile[0],thresold)
	velo = motionFreqDetect(freq)		
	point = motion2D(dist,velo)
	motionRecord(point,outfile)
	return point

if __name__ == "__main__":
	motionValueVerify("./initial1.csv",846.67,539.50)
	motionValueVerify("./initial1.csv",812.11,2202.64)
	motionValueVerify("./initial1.csv",1998.89,584.92)
	motionValueVerify("./initial1.csv",1615.35,1313.19)
