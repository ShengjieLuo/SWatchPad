from recordWave import *
from makeWave import *
from FFTtran import *
from FFThann import *
from analysisWave import *
from analysisWave2 import *
from IIR import *
from motion import *
from initial import *
from stateMachine import *
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy import interpolate

RECORD_CHUNK = 1024
RECORD_CHANNELS = 2
RECORD_RATE = 44100
RECORD_SECONDS_TOTAL = 10
RECORD_SECONDS_UNIT = 0.2
#RECORD_SECONDS_NUM = RECORD_SECONDS_TOTAL / RECORD_SECONDS_UNIT
RECORD_FILE_PATH = "/home/openstack/doppler/WAVE_04_19/"
RECORD_FILE_LIST = []
FREQ_LIST = []
FREQ_RECORD_INTERVAL = 5
FREQ_LEFT_LIMIT = 14000
FREQ_RIGHT_LIMIT = 18000
FREQ_WINDOW_SIZE = 33
#FREQ_LENGTH_ACTUAL = []
IIR_LEFT_LIMIT = 15900
IIR_RIGHT_LIMIT = 16000
INITIAL_STAT = []
INITIAL_FILE = ["./initial1.csv","./initial2.txt","./initial3.txt"]
ANALYSIS_PEAK_REF = [15975.4,16969.4] 
ANALYSIS_AROUND_WINDOW = 20
ANALYSIS_AROUND_FILE = "./peakAround.csv"
ANALYSIS_WEIGHT_FILE = "./weightAround.csv"
ANALYSIS_ITP_FILE = "./peakItp.csv"
ANALYSIS_PEAK = []
ANALYSIS_AROUND = []
ANALYSIS_AROUND_ITP = [] 
ANALYSIS_RESULT = []
MOTION_POINT = []
MOTION_THRESOLD = 0.01
MOTION_FILE = "./motionFile.csv"
MACHINE_THRESOLD = 2
MACHINE_FILE = './machineFile.csv'
MACHINE_POINT = []

#Import Function List
#def recordWave(CHUNK,CHANNELS,RATE,RECORD_SECONDS,WAVE_OUTPUT_FILENAME):
#def wavePeakIndex(FREQ_DATA,FREQ_WINDOW_SIZE):
#def weightAveragePeak(PEAK_AROUND,FILENAME,AROUND_WINDOW,TIME,INITIAL_PEAK):
#def valueInterpolate(PEAK_AROUND,TIME)
#def weightAverageAround(PEAK_AROUND,FILENAME,AROUND_WINDOW,TIME,INITIAL_PEAK):
#def motionDetection(AnaResult,StatInfo,initialFile):

def record():
	os.popen('rm -rf /home/openstack/doppler/WAVE_04_19')
	os.popen('mkdir /home/openstack/doppler/WAVE_04_19')
	num = int(RECORD_SECONDS_TOTAL/RECORD_SECONDS_UNIT)
	for i in range(num):
		FILENAME = RECORD_FILE_PATH + str(i)
		RECORD_FILE_LIST.append(FILENAME)
		print FILENAME
		recordWave(RECORD_CHUNK,RECORD_CHANNELS,RECORD_RATE,RECORD_SECONDS_UNIT,FILENAME)

'''
#old version
def freqInfo():
	for i in RECORD_FILE_LIST:
		xdata,ydata = fftHann(i,FREQ_LEFT_LIMIT,FREQ_RIGHT_LIMIT)
		FREQ_LIST.append([xdata,ydata]) 
'''


def freqInfo():
	for i in range(len(RECORD_FILE_LIST)-FREQ_RECORD_INTERVAL):	
		xdata,ydata,length = fftHann(RECORD_FILE_LIST,FREQ_LEFT_LIMIT,FREQ_RIGHT_LIMIT,FREQ_RECORD_INTERVAL,i) 
		FREQ_LIST.append([xdata,ydata])

def analysisInfo(flag=1):
	# flag = 0 : initial state
	# flag = 1 : test state
	for i in FREQ_LIST:
		peak1,peak2 = wavePeakIndex(i,FREQ_WINDOW_SIZE)
		peak1Around,peak2Around = wavePeakAround(i,peak1,peak2,ANALYSIS_AROUND_WINDOW)
		ANALYSIS_PEAK.append([peak1,peak2])
		ANALYSIS_AROUND.append([peak1Around,peak2Around])
		print [peak1,peak2]
	if flag==0:
		initialCSV(ANALYSIS_PEAK,INITIAL_FILE[0])
		initialStat(ANALYSIS_PEAK,INITIAL_FILE[1])
		initialPeak(ANALYSIS_PEAK,INITIAL_FILE[2])
		return 0
	ANALYSIS_PEAK_REF = loadPeak(INITIAL_FILE[2])	
	RECORD_SECONDS_NUM = int(RECORD_SECONDS_TOTAL / RECORD_SECONDS_UNIT - FREQ_RECORD_INTERVAL )
	printPeakAround(ANALYSIS_AROUND,ANALYSIS_AROUND_FILE,RECORD_SECONDS_NUM)	
	ANALYSIS_AROUND_ITP = valueInterpolate(ANALYSIS_AROUND,RECORD_SECONDS_NUM)
	printPeakAround(ANALYSIS_AROUND_ITP,ANALYSIS_ITP_FILE,RECORD_SECONDS_NUM)	
	#WeightAveragePeak(ANALYSIS_AROUND_ITP,ANALYSIS_WEIGHT_FILE,RECORD_SECONDS_NUM,ANALYSIS_PEAK_REF)
	ANALYSIS_RESULT = weightAveragePeak(ANALYSIS_AROUND_ITP,ANALYSIS_WEIGHT_FILE,RECORD_SECONDS_NUM,ANALYSIS_PEAK_REF,ANALYSIS_PEAK)
	return ANALYSIS_RESULT

def motion(ANALYSIS_RESULT):
	MOTION_POINT = motionDetection(ANALYSIS_RESULT,INITIAL_FILE,MOTION_FILE,MOTION_THRESOLD)
	for i in MOTION_POINT:
		print i
	print
	return MOTION_POINT	

def StateMachineCorrection(MOTION_POINT):
	MACHINE_POINT = SMCorrection(MOTION_POINT, MACHINE_THRESOLD) 
	SMRecord(MACHINE_POINT,MACHINE_FILE)
	for i in MACHINE_POINT:
		print i
	print
	return MACHINE_POINT

def mainFunc():
	record()
	freqInfo()
	ANALYSIS_RESULT = analysisInfo()
	MOTION_POINT = motion(ANALYSIS_RESULT)
	MACHINE_POINT = StateMachineCorrection(MOTION_POINT)

def initFunc():
	record()
	freqInfo()
	analysisInfo(0)

def main():
	if sys.argv[1]=='0':
		print "Initial FUnction"
		initFunc()
	elif sys.argv[1] == '1':
		print "Main Function"
		mainFunc()
	else:
		print "Wrong!"
	
if __name__ == "__main__":
	main()
