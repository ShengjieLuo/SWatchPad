import numpy as np
import pylab as pl
from scipy import interpolate
import matplotlib.pyplot as plt

def wavePeakAround(FREQ_DATA,PEAK1,PEAK2,AROUND_WINDOW):
	energy_list = FREQ_DATA[1]
	freq_list = FREQ_DATA[0]
	PEAK1_AROUND , PEAK2_AROUND = [],[]
	for i in range(PEAK1[0]-AROUND_WINDOW,PEAK1[0]+AROUND_WINDOW): 
		PEAK1_AROUND.append([i,freq_list[i],energy_list[i]])
	for i in range(PEAK2[0]-AROUND_WINDOW,PEAK2[0]+AROUND_WINDOW): 
		PEAK2_AROUND.append([i,freq_list[i],energy_list[i]])
	return PEAK1_AROUND,PEAK2_AROUND

def printPeakAround(PEAK_AROUND,FILENAME,TIME):
	fp = open(FILENAME,'w')
	string = []
	for i in range(TIME):
		string.append("")
	for i in range(TIME):
		for j in range(len(PEAK_AROUND[i][0])):
			string[i] += str(PEAK_AROUND[i][0][j][2]) + ","
		for j in range(len(PEAK_AROUND[i][1])):
                        string[i] += str(PEAK_AROUND[i][1][j][2]) + ","
		#print "string:",string[i]
	for i in string:
		fp.write(i)
		fp.write('\n')
	fp.close()

def weightAverageAround(PEAK_AROUND,FILENAME,TIME,INITIAL_PEAK):
	fp = open(FILENAME,'w')
	total1,total2 = 0,0
	count1,count2 = 0,0
	sum1,sum2 = 0,0
	for i in range(TIME):
		for j in range(len(PEAK_AROUND[i][0])):
			total1 += PEAK_AROUND[i][0][j][2] * PEAK_AROUND[i][0][j][1]
			#print PEAK_AROUND[i][0][j][2],PEAK_AROUND[i][0][j][1]
			sum1 += PEAK_AROUND[i][0][j][2]
			count1 += 1
		for j in range(len(PEAK_AROUND[i][1])):
			total2 += PEAK_AROUND[i][1][j][2] * PEAK_AROUND[i][1][j][1]
			sum2 += PEAK_AROUND[i][1][j][2]
			count2 += 1
		freq1 = total1/(sum1)-INITIAL_PEAK[0]
		freq2 = total2/(sum2)-INITIAL_PEAK[1]
		#print "Weight Average:"+str(freq1)+","+str(freq2)
		fp.write(str(freq1)+","+str(freq2)+'\n')
	fp.close()

def weightAveragePeak(PEAK_AROUND,FILENAME,TIME,INITIAL_PEAK,PEAK):
	fp = open(FILENAME,'w')
	total1 , total2 = 0.0,0.0
	sum1 , sum2 = 0.0,0.0
	result = []
	for i in range(TIME):
		for j in range(1,len(PEAK_AROUND[i][0])-1):
			if (PEAK_AROUND[i][0][j][2]>PEAK_AROUND[i][0][j-1][2]) and (PEAK_AROUND[i][0][j][2] > PEAK_AROUND[i][0][j+1][2]) and (PEAK_AROUND[i][0][j][2] > PEAK[i][0][2]*0.3):
				total1 += PEAK_AROUND[i][0][j][2] * PEAK_AROUND[i][0][j][1]
				print PEAK_AROUND[i][0][j][2],PEAK_AROUND[i][0][j][1]
				sum1 += PEAK_AROUND[i][0][j][2]
				#print "total1:",total1,"sum1",sum1
		for j in range(1,len(PEAK_AROUND[i][1])-1):
			if (PEAK_AROUND[i][0][j][2]>PEAK_AROUND[i][0][j-1][2]) and (PEAK_AROUND[i][0][j][2] > PEAK_AROUND[i][0][j+1][2]) and (PEAK_AROUND[i][1][j][2] > PEAK[i][1][2]*0.3):
				total2 += PEAK_AROUND[i][1][j][2] * PEAK_AROUND[i][1][j][1]
				print PEAK_AROUND[i][1][j][2],PEAK_AROUND[i][1][j][1]
				sum2 += PEAK_AROUND[i][1][j][2]
				#print "total2:",total2,"sum2",sum2
		#print "peak0",INITIAL_PEAK[0],"peak1",INITIAL_PEAK[1]
		freq1 = total1/sum1-INITIAL_PEAK[0]
		freq2 = total2/sum2-INITIAL_PEAK[1]
		energy1 = PEAK[i][0][2]
		energy2 = PEAK[i][1][2]
		print "Weight Average:"+str(freq1)+","+str(freq2)+","+str(energy1)+","+str(energy2)
		fp.write(str(freq1)+","+str(freq2)+","+str(energy1)+","+str(energy2)+'\n')
		result.append([freq1,freq2,energy1,energy2])
		total1 , total2 = 0.0 , 0.0
		sum1 , sum2 = 0.0 , 0.0
	fp.close()
	return result


def valueInterpolate(PEAK_AROUND,TIME,PLOT=0):
	PEAK_AROUND_ITP = []
	for i in range(TIME):
		valuelist1 , valuelist2 = [] , []
		indexlist1 , indexlist2 = [] , []
		freqlist1 , freqlist2 = [] , []
		indexlist1_new , indexlist2_new = [] , []
		freqlist1_new , freqlist2_new = [] , []
		temp_result1 , temp_result2 = [] ,[]
		for j in range(len(PEAK_AROUND[i][0])):
			valuelist1.append(PEAK_AROUND[i][0][j][2])
			indexlist1.append(PEAK_AROUND[i][0][j][1])
			freqlist1.append(PEAK_AROUND[i][0][j][0])
		for j in range(len(PEAK_AROUND[i][1])):
			valuelist2.append(PEAK_AROUND[i][1][j][2])
			indexlist2.append(PEAK_AROUND[i][1][j][1])
			freqlist2.append(PEAK_AROUND[i][1][j][0])
		x1 = np.array(indexlist1)
		#print x1
		y1 = np.array(valuelist1)
		x2 = np.array(indexlist2)
		y2 = np.array(valuelist2)
	
		for i in range(len(indexlist1)-1):
			for k in range(10):
				indexlist1_new.append(indexlist1[i]+k/10.0*(indexlist1[i+1]-indexlist1[i]))
				freqlist1_new.append(freqlist1[i]+k/10.0*(freqlist1[i+1]-freqlist1[i]))
		
		for i in range(len(indexlist2)-1):
			for k in range(10):
				indexlist2_new.append(indexlist2[i]+k/10.0*(indexlist2[i+1]-indexlist2[i]))
				freqlist2_new.append(freqlist2[i]+k/10.0*(freqlist2[i+1]-freqlist2[i]))
		
		x1_new , x2_new = np.array(indexlist1_new), np.array(indexlist2_new)
		#print len(indexlist1),len(indexlist1_new)
		#tck1 = interpolate.splrep(x1,y1)
		#bspline1 = interpolate.splev(x1_new,tck1)
		#tck2 = interpolate.sqlrep(x2,y2)
		#bspline2 = interpolate.sqlev(x2_new,tck2)
		itp1 = interpolate.spline(x1,y1,x1_new)		
		itp2 = interpolate.spline(x2,y2,x2_new)
		itp1 = list(itp1)
		itp2 = list(itp2)
		for j in range(len(indexlist1_new)):
			temp_result1.append([freqlist1_new[j],indexlist1_new[j],itp1[j]])
			temp_result2.append([freqlist2_new[j],indexlist2_new[j],itp2[j]])
		PEAK_AROUND_ITP.append([temp_result1,temp_result2])
		if PLOT == 1:
			plot1=plt.plot(x1,y1, 'b*',label='original values')
			plot2=plt.plot(x1_new, itp1, 'r-x',label='interped values')
			plt.xlabel('x axis')
			plt.ylabel('y axis')
			plt.legend()
			plt.show()
			plt.title('Spline')
			plt.savefig(str(i)+'.png')
	return PEAK_AROUND_ITP
		 		
def loadPeak(initialfile):
	fp = open(initialfile,'r')
	lines = fp.readlines()
	line = lines[0]
	line = line.strip()
	line = line.split(',')
	return [float(line[0]),float(line[1])]
							
