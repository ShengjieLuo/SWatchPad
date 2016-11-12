#coding:utf-8

'''
Name: TDoA
Effect: To calculate the Time Difference of Arrival (TDoA)
TDoA is a popular method to measure the 1D distance.
Give an example here: 
There are two different audio wave spreading path. The first path is from the speaker to the microphone directly,
and the second path is reflected by user's hand.
Obviously, two different spreading path would lead to the time difference of Arrival
The distance difference = time difference * audiowave velocity = point difference / sample rate * audiowave velocity
Version
0.1	Luo	Master branch
	The initial branch
'''

import csv

'''
Function:TDoA()
Effect: the key function in TDoA distance measuring

input1:	signalcsv	the name of the csv file within digital PSK signal 0/1
input2:	directpath	the length of direct path. Default value, 6 cm.
input3: samplerate	the samplerate of the wave file. Default value, 44100.
input4: additionalratio	the ratio (sample points after addition):(original sample points). Default value, 10.
input5:	debug		the debug flag. If debug = 1, verbose the debug information
output:	reflectpath	the length of the reflected path
'''

def TDoA(signalcsv,directpath = 6, samplerate = 44100, additionalratio = 10, debug = 0):
	psklist 	= _csv2list(signalcsv,debug)
	diff 		= _pointdiff(psklist,debug)
	distance 	= _point2distance(samplerate,additionalratio,diff,debug)
	reflect 	= _pathdistance(distance,directpath,debug)
	return reflect	

'''
FUnction: _csv2list()
input:	csvfile
input: 	debug
output:	psklist
'''
def  _csv2list(csvfile,debug): 
	reader = csv.reader(file(csvfile,'rb'))  
	for line in reader:
  		psklist = line
    	if debug==1:
		print "  [Debug]  Total number of digital PSK signals: ",len(psklist)
	return psklist

'''
Function: _pointdiff()
input:	psklist		the data structure of the PSK digital signal
input:	debug		debug flag. If debug = 1,verbose the debug infomation
output:	diff		the point difference of signals from two path
'''
def _pointdiff(psklist,debug=0):
	return 25


'''
Function: _point2distance()
Effect:	Translate the point difference into the distance difference
input1:	srate		the samplerate of the wave file. Default value, 44100.
input2:	ratio		the ratio (sample points after addition):(original sample points). Default value, 10.
input3:	diff		the point difference of signals from two path
#input4:	velocity	the velocity of the audio wave. Defualt value, 34300
input4:	debug		debug flag. If debug = 1,verbose the debug infomation
output:	distance	the distance we get.
'''
def _point2distance(srate,ratio,diff,debug):
	pointRate = srate * ratio	
	distance = (diff + 0.0) / pointRate * 34300.00
	if debug == 1:
		print "  [Debug]  The distance difference:(cm) ", distance
	return distance

'''
Function: _pathdistance
Effect:	Calculate the reflected distance
input1:	distanceDiff	the distance difference between two paths
input2:	directpath	the distance of the first direct path
output:	reflectpath	the distance of the second reflected path
'''
def _pathdistance(distanceDiff,directpath,debug):
	reflectpath = directpath + distanceDiff
	if debug == 1:
		print "  [Debug]  The distance of the Direct path(cm):  ",directpath
		print "  [Debug]  The distance of the Reflected path(cm): ",reflectpath
	return reflectpath

if __name__ == '__main__':
	TDoA('18000Hz_ideal.csv',debug=1)
