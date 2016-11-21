from readWave import _readwave
from readWave import showwave
import numpy as np
import csv

def _showdata(wavlist,csvname):
    csvfile = file(csvname, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(wavlist)
    csvfile.close()

'''
def demulti(wavename):
	listWave2=_readwave(wavename)
	xf=np.fft.fft(listWave2)
	len1=len(xf)
	for i in range(int(len1 * (16 / 44.1))):
		xf[i] = 0 + 0.00000000e+00j;
	for i in range(int(len1 * (19 / 44.1)),len1):
		xf[i] = 0 + 0.00000000e+00j;
	XF=np.fft.ifft(xf)
	return XF 
'''

def demulti(wavename):
	listWave2=_readwave(wavename)
	print "  [Debug] FFT-IFFT Begin!"
	xf=np.fft.fft(listWave2)
	print "test"
	len1=len(xf)
	for i in range(int(len1 * (0 / 44.1)),int(len1* (7 / 44.1))):
		xf[i] = 0 + 0.00000000e+00j
	print "  [Debug] FFT ready !"
	XF=np.fft.ifft(xf)
	print "  [Debug] IFFT ready!"
	return XF 

#def demulti(wavename):
	
