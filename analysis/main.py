#coding:utf-8

'''
Name : main.py
analysis部分的核心代码，用于衔接PSK测距的各个子程序，并且最终显示二维距离x,y
Version:
0.1	Luo	masterbranch
	the initial function
'''

from demodulate import dePSK_ideal as dePSK 
from TDoA import TDoA
from xymeasure import xydistance

def PSK2Dmain(wave1,wave2,l1,l2,samplerate,additionalratio,debug):
	signalcsv1 = wave1[:-4]+".csv"
	signalcsv2 = wave2[:-4]+".csv"
	dePSK(wave1,signalcsv1,debug)
	dePSK(wave2,signalcsv2,debug)
	distance1 = TDoA(signalcsv1,l1,samplerate,additionalratio,debug)
	distance2 = TDoA(signalcsv2,l2,samplerate,additionalratio,debug)
	x,y = xydistance(l1,l2,distance1,distance2)
	return x,y

def PSK1Dmain(wave,l,samplerate,additionalratio,debug):
	signalcsv = wave[:-4]+".csv"
	dePSK(wave,signalcsv,debug)
	distance = TDoA(signalcsv,l,samplerate,additionalratio,debug)
	return distance

if __name__=="__main__":
	#print PSK2Dmain('../makewave/18000Hz_10s_PSKSequenceZeroTwoPath.wav','../makewave/18000Hz_10s_PSKSequenceZeroTwoPath.wav',2.10,11.95,44100,10,1)
	print PSK1Dmain('./test11_13_2.wav',11.95,44100,10,1)
