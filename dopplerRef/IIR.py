#coding:utf-8
import scipy.signal as signal 
import numpy as np
import pylab as pl
import wave


def iir(SIGNAL,LEFT_LIMIT,RIGHT_LIMIT,SAMPLE_RATE,MAX_DB,MIN_DB):
	f0 = float(SAMPLE_RATE)/2
	left,right = LEFT_LIMIT/f0 , RIGHT_LIMIT/f0
	#stopleft , stopright = left/2 , (right+1)/2
	stopleft , stopright = left/2 , right+0.1
	band1 , band2 = signal.iirdesign([left,right],[stopleft,stopright],MIN_DB,MAX_DB)
	output = signal.lfilter(band2,band1,SIGNAL)
	out = 20*np.log10(np.abs(output))
	index = np.where(np.logical_and(out[1:-1] > out[:-2], out[1:-1] > out[2:]))[0] + 1
	print out
	# 绘制滤波之后的波形的增益
	t = np.arange(0, 1, 1/float(SAMPLE_RATE))
	pl.plot(t[index]*f0, out[index] )
	pl.title(u"频率扫描波测量的滤波器频谱")
	pl.ylim(100,400)
	pl.xlim(15500,16500)
	pl.ylabel(u"增益(dB)")
	pl.xlabel(u"频率(Hz)")

	pl.subplots_adjust(hspace=0.3)
	pl.show()

if __name__ == "__main__":
	t = np.arange(0,2,1/8000.0)
	sweep = signal.chirp(t,f0=0,t1=2,f1=4000.0)
	out = iirFilter(sweep,1000.0,3000.0,8000.0,40,2)
	out = np(out)
	#index = np.where(np.logical_and(out[1:-1]>out[:-2],out[1:-1]>out[2:]))[0]+1
	#pl.plot(t[index]/2.0*4000,out[index])
	pl.plot(t/2.0*4000,out)


def iirFilter(name,leftlimit,rightlimit,flag=0):
	wf = wave.open(name, "rb")
	nframes = wf.getnframes()
	framerate = wf.getframerate()
	print "framerate:",framerate
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
	print wave_data2
	iir(wave_data2,leftlimit,rightlimit,framerate,100,50)

