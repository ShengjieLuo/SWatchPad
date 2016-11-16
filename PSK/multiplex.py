from readWave import _readwave
from readWave import showwave
import numpy as np
import csv

def _showdata(wavlist,csvname):
    csvfile = file(csvname, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(wavlist)
    csvfile.close()

def demulti(wavename):
	listWave2=_readwave(wavename)
	xf_complex=np.fft.fft(listWave2)
	for i in range(int(441000*(16.5/44)),int(441000*(17.5/44))):
		xf_complex[i]=0+0.00000000e+00j;# remove the 17Khz in Frequency domain
	XF_complex=np.fft.ifft(xf_complex)
	return XF_complex




