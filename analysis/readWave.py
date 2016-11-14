#coding:utf-8
import wave
import math
import numpy as np
import csv

'''
Name: readWave.py
Function: Be used to read the wave file and transform the wave file to an identified data structure
说明：本程序用于读取录音文件，并且将录音文件转化为csv文件的格式。
CSV文件格式可以直接在excel中打开，便于数据可视化
'''


'''
Function: wave2csv(inputname,outputname)
说明：用于读取录音得到的WAV文件，并将其打印到csv文件中
Input1: inputname: the filename of the input WAV
Input2: outputname: the filename of the output CSV
Version:
0.1	Luo	master branch	11/10
	The initial version
'''
def wave2csv(inputname,outputname):
	wavlist = _readwave(inputname)
	_list2csv(wavlist,outputname)


'''
Function: wave2csv(inputname)
说明：用于读取录音得到的WAV文件，并将其以list的结构输出
Input1: inputname: the filename of the input WAV
Version:
0.1     Luo     master branch   11/10
        The initial version
'''
def wave2list(inputname):
	return _readwave(inputname)
	

'''
FUnction: _readwave(inputname)
说明：用于实际读取的私有函数
Input1: inputname: the filename of the input WAV
Version:
0.1	Luo	master branch	11/10
	the initial version
'''
def _readwave(inputname):
        count = 0
        wavname = inputname
        wf = wave.open(wavname, "rb")
	nframes = wf.getnframes()
	framerate = wf.getframerate()
	str_data = wf.readframes(nframes)
        wf.close()
        wave_data = np.fromstring(str_data, dtype=np.short)
        wave_data = wave_data.T
	wave_list = wave_data.tolist()
	#print wave_list[2000:6000]
	#print len(wave_list)
	return wave_list

'''
Function:_list2csv(wavlist)
说明：用于将wavList转化为csv
INput1: wavlist: the list type of the wav file
Version:
0.1	lUO	master branch	11/10
	the initial version
'''
def _list2csv(wavlist,csvname):
	csvfile = file(csvname, 'wb')
	writer = csv.writer(csvfile)
	writer.writerow(wavlist)
	csvfile.close()

def showwave(wavfile):
	wavlist = wave2list(wavfile)
	wavlist = wavlist[:1000]
	_list2csv(wavlist,wavfile[:-4]+"_show1000points.csv")	

if __name__=="__main__":
	#wave2list("1.wav")
	#wave2list("seqPSK.wav")
	#wave2csv("2000_test.wav","2000_test.csv")
	showwave('18000Hz_10s_1.5p_PSKSequenceZeroTwoPath.wav')
	showwave('18000Hz_10s_1p_PSKSequenceZeroTwoPath.wav')
	showwave('18000Hz_10s_2p_PSKSequenceZeroTwoPath.wav')
	
	
