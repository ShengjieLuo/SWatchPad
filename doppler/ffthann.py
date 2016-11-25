# -*- coding: utf-8 -*-
'''
Name: fft.py
Function: DO the fft transformation. 
说明：本程序用于进行FFT变换，使得时域信号转化为频域信号。通过分析频域信号，可以确定当前声音信号的频率。
Version:
0.1	Luo	master branch
	The initial version
'''

import numpy as np
import matplotlib
import wave
import scipy.signal as signal

'''
Function: ffttran()
说明：用于对给定的WAV文件进行FFT变换，并且返回频域信息
input1:	name		the filename of the WAV file
input2:	leftlimit	left limit of the frequency domain signal
input3:	rightlimit	right limit of the freuqency domain signal
input4: flag		flag=1 verbose the debug infomation

output1: xdata		the frequency axis
output2: ydata		the energy axis

Version:
0.1     Luo     master branch
        THe initial version
'''

def ffttran(name,start,N,leftlimit,rightlimit,flag=0):
	#matplotlib.use('Agg') 
	wf = wave.open(name, "rb")
	nframes = wf.getnframes()
	framerate = wf.getframerate()
	'''
	if flag==1:
		print "  [Debug]  Totally Frames: ",nframes
		print "  [Debug]  The Framerate of the audio file: ",framerate
	'''
	str_data = wf.readframes(framerate)
	wf.close()
	wave_data = np.fromstring(str_data, dtype=np.short)
	#N=len(wave_data)
	start=0 #开始采样位置
	df = framerate/(N-1.0) # 分辨率
	if flag==1:
		print "  [Debug]  The difiniton rate(frequency range per index point): ",df
	freq = [df*n for n in range(0,N)] #N个元素
	wave_data2 = wave_data[start:start+N]
	wave_data2 = wave_data2 * signal.hann(N,sym=0)*2
	c=np.fft.fft(wave_data2)*2/N
	index_begin = _waveIndexBegin(freq,c,leftlimit)
	index_end = _waveIndexEnd(freq,c,rightlimit)
	xdata,ydata = _waveFreqData(name,freq,c,index_begin,index_end,N)
	#'''
	if flag==1:
		print "  [Debug]  The Primary Frequency Peak"
		for i in range(len(xdata)):
			if ydata[i]>100:
				print "    freq: "+str(xdata[i])+" energy: "+str(ydata[i])
	#'''
	return xdata,ydata

'''
Function: _waveINdexBegin
说明： 这是一个ffttran用到的私有函数
Version:
0.1	Luo	master branch
	THe initial version
'''
def _waveIndexBegin(freq,c,leftlimit):
        index_begin = 0
        while freq[index_begin]<leftlimit:
                index_begin += 10
        return index_begin

'''
Function: _waveIndexEnd
说明： 这是一个ffttran用到的私有函数
Version:
0.1     Luo     master branch
        THe initial version
'''
def _waveIndexEnd(freq,c,rightlimit):
        index_end = int(len(c)/2)
        while freq[index_end]>rightlimit:
                index_end -= 10
        return index_end

'''
Function: _waveFreqData
说明： 这是一个ffttran用到的私有函数
Version:
0.1     Luo     master branch
        THe initial version
'''
def _waveFreqData(name,freq,c,index_begin,index_end,length):
        x_data = []
        for i in freq[index_begin:index_end-1]:
                x_data.append(i*44100.0/length)
        energy_data = abs(c[index_begin:index_end-1])
        y_data = []
        for i in energy_data:
                y_data.append(i)
        return x_data,y_data

if __name__=='__main__':
	#fftHann('18000Hz_10s_PSKSequenceZero.wav',0,20000,1)
	ffttran('test11_13_2.wav',0,20000,1)
