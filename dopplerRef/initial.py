

def initialCSV(PeakInfo,initialfile):
	# input:peak info (time,freq,value)
	# output: Peak Data Statistical data(average,difference)
	fp = open(initialfile,'w')
	#str1 = "channel1,"
	#str2 = "channel2,"
	str1 , str2 ,str0 = "","",""
	for i in range(len(PeakInfo)):
		str0 += str(i) + ","
		str1 += str(PeakInfo[i][0][2]) + ","
		str2 += str(PeakInfo[i][1][2]) + ","
	str0 = str0[:-1]
	str1 = str1[:-1]
	str2 = str2[:-1]
	str0 += '\n'
	str1 += '\n'
	str2 += '\n'
	fp.write(str0)
	fp.write(str1)
	fp.write(str2)
	fp.close()

def initialStat(PeakInfo,initialfile):
	fp = open(initialfile,'w')
	sum1,count1 = 0,0
	sum2,count2 = 0,0
	for i in range(len(PeakInfo)):
		sum1 += PeakInfo[i][0][2]
		sum2 += PeakInfo[i][1][2]
		count1 += 1
		count2 += 1
	avg1 = sum1/float(count1)
	avg2 = sum2/float(count2)
	sum1, sum2 = 0,0
	for i in range(len(PeakInfo)):
		sum1 += (PeakInfo[i][0][2]-avg1) ** 2
		sum2 += (PeakInfo[i][1][2]-avg2) ** 2
	Devial1 = (sum1/count1) ** 1/2
	Devial2 = (sum2/count2) ** 1/2
	stat = str(avg1)+','+str(avg2)+','+str(Devial1)+','+str(Devial2)+'\n'
	fp.write(stat)
	fp.close()
	return [avg1,avg2,Devial1,Devial2]

def initialPeak(PeakInfo,initialfile):
	fp = open(initialfile,'w')
	sum1,count1 = 0,0
	sum2,count2 = 0,0
	for i in range(len(PeakInfo)):
		sum1 += PeakInfo[i][0][1]
		sum2 += PeakInfo[i][1][1]
		count1 += 1
		count2 += 1
	avg1 = sum1/count1
	avg2 = sum2/count2
	peak = str(avg1)+','+str(avg2)
	fp.write(peak)
	fp.close()
