#coding:utf-8

import numpy as np
import matplotlib
import wave

def fftWave(name,leftlimit,rightlimit,flag=0):
	#matplotlib.use('Agg') 
	wf = wave.open(name, "rb")
	nframes = wf.getnframes()
	framerate = wf.getframerate()
	str_data = wf.readframes(nframes)
	wf.close()
	wave_data = np.fromstring(str_data, dtype=np.short)
	wave_data.shape = -1,2
	wave_data = wave_data.T
	N=len(wave_data[0])
	start=0 #开始采样位置
	df = framerate/(N-1) # 分辨率
	freq = [df*n for n in range(0,N)] #N个元素
	wave_data2=wave_data[0][start:start+N]
	c=np.fft.fft(wave_data2)*2/N
	index_begin = waveIndexBegin(freq,c,leftlimit)
	index_end = waveIndexEnd(freq,c,rightlimit)
	xdata,ydata = waveFreqData(name,freq,c,index_begin,index_end)
	if flag==1:
		for i in range(len(xdata)):
			if ydata[i]>1:
				print "freq:"+str(xdata[i])+" energy:"+str(ydata[i])
	return xdata,ydata

def waveIndexBegin(freq,c,leftlimit):
	index_begin = 0
	while freq[index_begin]<leftlimit:
		index_begin += 10
	return index_begin

def waveIndexEnd(freq,c,rightlimit):
	index_end = int(len(c)/2)
	while freq[index_end]>rightlimit:
		index_end -= 10
	return index_end

def waveFreqData(name,freq,c,index_begin,index_end):
	x_data = freq[index_begin:index_end-1]
	energy_data = abs(c[index_begin:index_end-1])
	y_data = []
	for i in energy_data:
		y_data.append(i)
	return x_data,y_data

if __name__=="__main__":
	fftWave("../WAVE_04_19/1",3000,7000)	
		
	
