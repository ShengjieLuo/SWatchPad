#coding:utf-8

'''
Name: demodulate.py
说明：本程序用于对PSK的波形进行解调，即包括完美的PSK波形，也包括实际接收到的有瑕疵的PSK波形
Version
0.1	Luo	master branch
	THe initial version
0.2	Luo	master branch
	1. Cutoff the '_regulate' function and return the 'digital signal' directly.
	2. Add the debug flag to enable the debug mode
	3. Test the suitable num in function '_signaltest'
'''

import csv
import wave
import numpy as np
import pylab as pl
import pdb
from scipy import interpolate 
from readWave import wave2list as readWave_wave2list
from multiplex import demulti as _demulti
from fft import ffttran as fft_ffttran
 
'''
FUnction: dePSK_ideal(wavlist)
说明：用于对理想状态下的PSK波形进行解码，主要用于测试解码程序的正确性
'''
def dePSK_ideal(wavfile,outputfile,debug=0):
	ratio = 10
	wavlist = _wav2list(wavfile)
	#reffreq = _getRefFreq(wavfile,debug)
	reffreq = 18000
	wavlistFilter = _listfilter(wavlist,debug)
	wavlistAdd = _freqadd(wavlistFilter,ratio,debug)
	digitalsignal = _demodulate(wavlistAdd,reffreq,ratio,debug)
	#_signaltest(digitalsignal,ratio,debug)
	#PSKsignal = _regulate(digitalsignal,debug)
	_list2csv(digitalsignal,outputfile)
	return digitalsignal

def dePSK_multi(wavfile,reffreq,outputfile,debug=0):
	ratio = 10
	wavlist = _demulti(wavfile)
        wavlistFilter = _listfilter(wavlist,debug)
        wavlistAdd = _freqadd(wavlistFilter,ratio,debug)
        digitalsignal = _demodulate(wavlistAdd,reffreq,ratio,debug)
        _list2csv(digitalsignal,outputfile)
        return digitalsignal
	
'''
Function: _wav2list()
说明：私有函数，用于将csv格式的数据转化为List数据结构
input:	wavname		the name of the wav file
output:	wavlist		the data structure of the wave
'''
def _wav2list(wavname):
	return readWave_wave2list(wavname)

'''
Functiuon:_listfilter()
说明：我们采集到的list前面有一部分是0,初始部分的信号质量也不好，所以需要过滤出有效的部分
input:	wavlist		the data structure of the original audio sample
output:	wavlistFilter	the data structure of the filtered audio sample
'''
def _listfilter(wavlist,debug=0):
	wavlistFilter = []
	flag = 0
	for i in wavlist:
		if flag == 1:
			wavlistFilter.append(i)
		elif flag == 0 and (i>10 or i<-10):
			wavlistFilter.append(i)
			flag = 1
		else:
			continue
	if debug == 1:
		print "  [Debug]  The length before filter:",len(wavlist)
		print "  [Debug]  The length after filter:",len(wavlistFilter)	
	return wavlistFilter


'''
Function: _getRefFreq()
说明：由于PSK的解码和声波的频率有关，因而我们需要获得声波信号的参考频率用于解码，这一步可以直接调用FFT的结果
input:	wavfile		the name of the wave file
output:	reffreq		reference frequency of the audio signal
'''
def _getRefFreq(wavfile,debug=0):
	freqdata,energydata = fft_ffttran(wavfile,16000,20000,flag=1)
	peakcount , peaksum = 0 ,0 
	for i in range(1,len(freqdata)-1):
		if energydata[i]>100 and energydata[i]>energydata[i-1] and energydata[i]>energydata[i+1]:
			peakcount += energydata[i]
			peaksum += energydata[i]*freqdata[i]
	reffreq = (peaksum+0.0)/peakcount
	if debug==1:
		print "  [Debug]  Reference Frequency: ",reffreq
	return reffreq

'''
FUnction: _freqadd()
说明：由于初始的频率点是十分稀疏的，这不利于PSK的解码工作，所以我们需要在两个采样点之间增添一些辅助采样点，用于提高PSK的精度
input:	wavlist		the data structure of the filtered audio sample
input: 	ratio		The points after addition : The points before addtion. By default, ratio = 10
input: 	debug		verbose the debug information if debug = 1
output:	wavlistadd	the data structure of the addtional audio samples
'''
def _freqadd(wavlist,ratio=10,debug=0):
	# The ratio should be integer larger than 1 -- note by SHengjie
	y = wavlist
	x = np.linspace(1,len(wavlist),len(wavlist))
	x_new = np.linspace(1,len(wavlist),len(wavlist)*ratio)
	tck = interpolate.splrep(x, y)
	y_bspline = interpolate.splev(x_new, tck)
	if debug == 1:
		print "  [Debug]  Points after addition:",len(y_bspline)
		fp = open("test.csv","wb")
		string = ""
		for i in range(1000000+9000,1000000+11000):
			string = string + str(y_bspline[i]) +"\n"
		fp.write(string)
		fp.close()
	return y_bspline

'''
Function: _demodulate()
说明：这个私有函数是PSK解调的关键函数，用于PSK直接解调为数字信号
input:	wavlist		the data structure of the filtered additional audio sample
input:	ref		the reference frequency
output:	signallist	the data structure of the demodulated digital signal
'''
def _demodulate(wavlist,reffreq,ratio=10,debug=1):
	sampleRate = 44100.0*ratio 		#经过处理后，每秒采样的个数
	cycleRate = reffreq			#每秒采样的周期数
	point_per_cycle = sampleRate/cycleRate	#每个周期对应的采样点个数
	wavlist_original = wavlist[int(round(point_per_cycle)):] #原始波形
	wavlist_difference = wavlist[:int(len(wavlist)-round(point_per_cycle))] #差分相干波形
	if debug == 1:
		print "  [Debug]  Sample point per signal cycle: ",point_per_cycle
	digitalsignal = []
	for i in range(len(wavlist_original)):
		flag = wavlist_original[i]*wavlist_difference[i]
		if flag>=0:
			digitalsignal.append(1)
		else:
			digitalsignal.append(0)
	#_test(digitalsignal)
	if debug == 1:
		fp = open("test2.csv","wb")
                string = ""
                for i in range(1020600,1022350):
                        string = string + str(digitalsignal[i]) +"\n"
                fp.write(string)
                fp.close()
	digitalsignal = digitalsignal[1000000:]
	return digitalsignal

'''
Function:_list2csv()
说明：transform the list structure to csv file
input:	signallist
output:	csvname
'''
def _list2csv(signallist,csvname):
	csvfile = file(csvname, 'wb')
        writer = csv.writer(csvfile)
        writer.writerow(signallist)
        csvfile.close()

'''
Function:_signaltest()
说明：这个函数可以粗略地检验解调结果是否符合我们的预期。
程序将会打印出一个检验数组，理论上这个数组是一个从2开始的等差数列
结果越接近这个等差数列，那么解调结果越理想;反之，则越差
input:	digitalsignal	list of the digital signals after modulated
output:	newlist		the regulated list
'''
def _signaltest(digitalsignal,ratio,debug=0):
	num = 5
	#Note : For ideal signal, the 'num' should be 5 --From Shengjie
	target = [0]*num
	verifylist = []
	for i in range(len(digitalsignal)-5):
		if digitalsignal[i:i+num] == target:
			verifylist.append(i/ratio)
	newlist = list(set(verifylist))
	newlist.sort()
	verifylist,tmplist = [],[]
	for i in range(len(newlist)-1):
		verifylist.append((newlist[i+1]-newlist[i])/49)
		#if newlist[i+1]-newlist[i]>130:
		#	break
	for i in range(len(verifylist)):
		if verifylist[i] != 0:
			tmplist.append(verifylist[i])
		if verifylist[i] >= 130:
			break
	verifylist = tmplist
	if debug == 1:
		print "  [Debug]  The interval between two ZERO signal: ",verifylist
	return newlist

'''
Function:_regulate()
说明：用于规整格式
'''
def _regulate(digitalsignal,ratio=10,debug=0):
	length = len(digitalsignal)/ratio
	PSKsignal = [1]*length
	num = 20
        target = [0]*num
        for i in range(len(digitalsignal)-5):
                if digitalsignal[i:i+num] == target:
                        PSKsignal[i/ratio]=0
	return PSKsignal


if __name__ == '__main__':
	#dePSK_ideal('../makewave/18000Hz_10s_PSKSequenceZero.wav','18000Hz_ideal.csv',debug=1)
	dePSK_ideal('../makewave/18000Hz_10s_PSKSequenceZeroTwoPath.wav','18000Hz_ideal_twopath.csv',debug=1)
	#dePSK_ideal('18000_test.wav','18000Hz_test.csv',debug=1)
	#dePSK_ideal('18000_hand.wav','18000_hand.csv',debug=1)
	#dePSK_multi('../testwave/11-18/Name18No.wav.wav',18000,'../testwave/11-18/Name18No.wav.csv',debug=1)
