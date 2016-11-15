from scipy import stats
import math
import pandas as pd

def motionValueTest(Peak,initialFile):
	# input: peak value, statInfo
	# output: whether it is a singular value
	PeakData = pd.read_csv(initialFile)
	print "#1 data.describe"
	#print PeakData.describe()
	print "#2 data.describe"
	PeakData =  PeakData.T
	#print PeakData
	print "#3 data.test"
	print PeakData.describe()
	channel1 = PeakData.ix[:,0]
	channel2 = PeakData.ix[:,1]
	print channel1
	print channel2
	testResult1 = stats.ttest_1samp(a=channel1,popmean=Peak[0])
	testResult2 = stats.ttest_1samp(a=channel2,popmean=Peak[1])
	print "testResult1:",testResult1[1]
	print "testResult2:",testResult2[1]

if __name__ == "__main__":
	motionValueTest([680,1000.0],"initial1.csv")
