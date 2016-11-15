from scipy import stats as ss
import math
import pandas as pd

#data[i][0,1,2,3]
#ref[0,1][0,1]

def initialPeak(PeakInfo):
	# input:peak info (time,freq,value)
	# output: Peak Data Statistical data(average,difference)
	sum1,count1 = 0
	sum2,count2 = 0
	for i in range(len(PeakInfo)):
		sum1 += PeakInfo[i][0][2]
		sum2 += PeakInfo[i][1][2]
		count1 += 1
		count2 += 1
	avg1 = sum1/float(count1)
	avg2 = sum2/float(count2)
	sum1, sum2 = 0
	for i in range(len(PeakInfo)):
		sum1 += (PeakInfo[i][0][2]-avg1) ** 2
		sum2 += (PeakInfo[i][1][2]-avg2) ** 2
	Devia1 = (sum1/count1) ** 1/2
	Devia2 = (sum2/count2) ** 1/2
	return [avg1 , avg2, Devial1 , Devial2 ]

def motionValueTest(Peak,PeakInfo):
	# input: peak value, statInfo
	# output: whether it is a singular value
	fp = open("motionValueTest.csv",'w')
	str1 = "channel1,"
	str2 = "channel2,"
	for i in range(len(PeakInfo)):
		str1 += str(PeakInfo[i][0][2]) + ","
		str2 += str(PeakInfo[i][1][2]) + ","
	str1 += '\n'
	str2 += '\n'
	fp.write(str1)
	fp.write(str2)
	PeakData = pd.read_csv("motionValueTest.csv")
	print "#1 data.describe"
	PeakData.describe()
	print "#2 data.describe"
	PeakData.T
	PeakData.describe()
	print "#3 data.test"
	channel1 = df.ix[:,'channel1']
	channel2 = df.ix[:,"channel2"]
	testResult1 = stats.ttest_1samp(a=channel1,popmain=Peak[0][2])
	testResult2 = stats.ttest_1samp(a=channel2,popmain=Peak[1][2])
	isValue = []
	if testResult1[1]<0.05:
		isValue.append(1)
	else:
		isValue.append(0)
	if testResult2[1]<0.05:
		isValue.append(1)
	else:
		isValue.append(0)
	return isValue

def motionEnergyDistance(Peak,Flag,StatInfo):
	# input: peak value, statInfo , isValueFlag
	# output: distance of different channel1
	for i in range(len(Peak)):
		Flag = motionValueTest(Peak,)
	return [dist1,dist2]


def motionDetectionEnergy(Peak,StatInfo):
	# input: peak value
	# output: channel1 distance, channel2 distance
	EnergyInfo = []
	for i in range(len(Peak)):
		flag = motionValueTest(Peak,StatInfo)
		height1 , height2 = motionEnergyDistance(Peak,flag,StatInfo)	
		EnergyInfo.append([height1,height2])
	return EnergyInfo
	
def motionDetectionFreq(Freq):
	# input:  Fre
	

	
def motionDetection(Info,StatInfo):
	Peak = []
	Freq = []
	for i in Info:
		Peak.append([Info[i][2],Info[i][3]])
		Freq.append([Info[i][0],Info[i][1]])
	EnergyInfo = motionDetectionEnergy(Peak,StatInfo)
	FreqInfo = motionDetectionFreq(Freq,StatInfo)
