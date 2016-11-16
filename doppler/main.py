import sys
from ffthann import ffttran as _fft
from peak import waveFreqShift as _freqshift
from readWave import wavelength as _wavelength

def dopplerMain(wavfile,debug=0):

	leftLimit = 16000
	rightLimit = 18000
	scanWindow = 100
	peakWindow = 33
	peakRef = 17000
	step = 4410 
	samples = 44100
	length = _wavelength(wavfile)
	freqShiftList = []
	
	for start in range(0,length-samples-1,step):
		x_data , y_data = _fft(wavfile,start,samples,leftLimit,rightLimit)		
		freqShift = _freqshift(x_data,y_data,peakRef,scanWindow,peakWindow)
		freqShiftList.append(freqShift)
	if debug==1:
		print "  [Debug]  Frequency Shift in Audio Sample: ",freqShiftList

if __name__=='__main__':
	dopplerMain(sys.argv[1],debug=1)
