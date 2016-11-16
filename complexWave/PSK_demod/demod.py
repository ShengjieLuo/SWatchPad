from readWave import _readwave
from readWave import showwave
import numpy as np
import csv

def showdata(wavlist,csvname):
    csvfile = file(csvname, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(wavlist)
    csvfile.close()

listWave=_readwave('18000Hz_10s_PSKBalanceZero.wav')
listWave2=_readwave('18000Hz_10s_PSKComplexBalanceZero.wav')

showwave('18000Hz_10s_PSKBalanceZero.wav')
showwave('18000Hz_10s_PSKComplexBalanceZero.wav')

#test for pure 18Khz PSK ->fft -> ifft ->original 18Khz PSK?
xf_balance = np.fft.fft(listWave)
XF_balance = np.fft.ifft(xf_balance)
showdata(XF_balance,'test_for_single.csv')
# if it's correct, test_for_single.csv should be almost the same to 18000Hz_10s_PSKBalanceZero.csv


#test for 17Khz+18Khz ->fft and kill 17Khz ->ifft -> pure 18Khz?
xf_complex=np.fft.fft(listWave2)

for i in range(int(441000*(16.5/44)),int(441000*(17.5/44))):
    xf_complex[i]=0+0.00000000e+00j;# remove the 17Khz in Frequency domain

XF_complex=np.fft.ifft(xf_complex)
showdata(XF_complex,'test_for_complex.csv')
# if this method can filter17Khz, test_for_complex.csv should be the same to 18000Hz_10s_PSKBalanceZero.csv ,but its not.




