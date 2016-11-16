import sys
from ffthann import ffttran as _fft
from peak import waveFreqShift as _freqshift
from readWave import wavelength as _wavelength
from velocity import VelocityCal as _velocity

def dopplermain(wavfile1,wavfile2,x0,y0,debug=0):

	leftLimit = 16000
	rightLimit = 18000
	scanWindow = 100
	peakWindow = 33
	peakRef = 17000
	step = 4410 
	samples = 44100
	length = _wavelength(wavfile1)
	freqShiftList,locationList = [],[]
	x,y = x0,y0
	
	for start in range(0,length-samples-1,step):
		x_data , y_data = _fft(wavfile1,start,samples,leftLimit,rightLimit)		
		freqShift1 = _freqshift(x_data,y_data,peakRef,scanWindow,peakWindow)
		
		x_data , y_data = _fft(wavfile2,start,samples,leftLimit,rightLimit)		
		freqShift2 = _freqshift(x_data,y_data,peakRef,scanWindow,peakWindow)
		
		freqShiftList.append([freqShift1,freqShift2])
		vx , vy = _velocity(freqShift1,freqShift2,peakRef,x,y)
		x = x + vx/(samples/step)
		y = y + vy/(samples/step)
		locationList.append([x,y])
		
	if debug==1:
		print "  [Debug]  Frequency Shift in Audio Sample: ",freqShiftList
		print "  [Debug]  The location lists detected: ",locationList

if __name__=='__main__':
	dopplerMain(sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),debug=1)
