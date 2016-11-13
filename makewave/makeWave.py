#coding:utf-8


'''
makewave.py
作用：用于制作需要的音频文件
说明：
本程序用于制作音频文件的库是python的wave库，请参考以下链接
https://docs.python.org/2/library/wave.html
主要函数如下
Wave_write.setnchannels(n)		设定声道数量Set the number of channels.
Wave_write.setframerate(n)		设定帧率Set the frame rate to n.
Wave_write.setnframes(n)		设定帧的数量Set the number of frames to n. This will be changed later if more frames are written.
Wave_write.setcomptype(type, name) 	设定压缩方式Set the compression type and description. At the moment, only compression type NONE is supported.
Wave_write.setparams(tuple)             设定基本参数The tuple should be (nchannels, sampwidth, framerate, nframes, comptype, compname)
Wave_write.tell()                       显示基本参数Return current position in the file, with the same disclaimer for the Wave_read.tell() and Wave_read.setpos() methods.
Wave_write.writeframesraw(data)		实际写文件 Write audio frames, without correcting nframes.
Wave_write.writeframes(data)		实际写文件 Write audio frames and make sure nframes is correct.
'''

import wave
#import pyaudio
import math
import struct



'''
Function: SimpleDoubleWaveMake(freq1,freq2,time)
Effect: make the soundwave file with simple wave and two channels
Input1: freq1 the frequency used in channel1
Input2: freq2 the frequency used in channel2
Input3: time length of the audio
Output: the filename of the audio file
Version:
0.1	master branch	Author:luo	Date:11/09
	the fundamental version
'''
def simpleDoubleWaveMake(freq1,freq2,time):
	MAX_AMPLITUDE = 32767
	SAMPLE_RATE = 44100 
	DURATION_SEC = 	time
	SAMPLE_LEN = SAMPLE_RATE * DURATION_SEC
	filename = './'+ str(freq1) + 'Hz_' + str(freq2)+ 'Hz_'+ str(DURATION_SEC) + 's_simple_double.wav'
	print "Creating sound file:", filename
	print "Sample rate:", SAMPLE_RATE
	print "Duration (sec):", DURATION_SEC
	print "# samples:", SAMPLE_LEN
	wavefile = wave.open(filename, 'w') 
	wavefile.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed')) 
	samples = []    
	for i in range(SAMPLE_LEN):
    		t = float(i) / SAMPLE_RATE  
    		sample = MAX_AMPLITUDE * math.sin(t * freq1 * 2 * math.pi) 
    		packed_sample = struct.pack('h', sample) 
    		samples.append(packed_sample)  
    		sample2 = MAX_AMPLITUDE * math.sin(t * freq2 * 2 * math.pi)
    		packed_sample2 = struct.pack('h', sample2)	
    		samples.append(packed_sample2)  
   	sample_str = ''.join(samples)  
	wavefile.writeframes(sample_str)
	wavefile.close()    
	return filename


'''
Function: SimpleSingleWaveMake(freq,time)
Effect: make the soundwave file with simple wave and single channel
Input1: freq: the frequency of the required waves
Input2: time: length of the audio
Output: the filename of the audio file
Version:
0.1 	matster branch	Author:Luo	Data:11/09
	the fundamental version
'''
def SimpleSingleWaveMake(freq,time):
	MAX_AMPLITUDE = 32767
        SAMPLE_RATE = 44100
        DURATION_SEC =  time
        SAMPLE_LEN = SAMPLE_RATE * DURATION_SEC
        filename = './'+ str(freq) + 'Hz_'+ str(DURATION_SEC) + 's_simple_single.wav'
        print "Creating sound file:", filename
        print "Sample rate:", SAMPLE_RATE
        print "Duration (sec):", DURATION_SEC
        print "# samples:", SAMPLE_LEN
        wavefile = wave.open(filename, 'w')
        wavefile.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
        samples = []
        for i in range(SAMPLE_LEN):
                t = float(i) / SAMPLE_RATE
                sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi)
                packed_sample = struct.pack('h', sample)
                samples.append(packed_sample)
        sample_str = ''.join(samples)
        wavefile.writeframes(sample_str)
        wavefile.close()
        return filename

'''
Function:PSKSimpleZeroWaveMake(freq,time)
Effect: TO make a simple PSK sound wave, we require a phase convert in the audio sample, in this function, we would make an audio with one phase convertion in the middle of the it
说明：PSK的音频信号和简谐音频信号的不同是，在音频中会有若干处地方，出现相位角180度的偏转，这个函数将会制作一个典型的2PSK信号。
对于一段时间长度为t的声音信号，将在t/2处产生一个相位翻转，这是一个典型的数字调相信号，它传递的信息是11111...11011...111
Input1: freq : frequency of the required audio file
Input2: time : the time length of the audio file
Output: the filename of the audio file
Version:
0.1	master branch	Author:Luo	Date:11/09
'''
def PSKSimpleZeroWaveMake(freq,time):
	MAX_AMPLITUDE = 32767	
	SAMPLE_RATE = 44100
	DURATION_SEC = time
	SAMPLE_LEN =  SAMPLE_RATE * DURATION_SEC
	filename = './'+ str(freq) + 'Hz_'+ str(DURATION_SEC) + 's_PSKSimpleZero.wav'
        print "Creating sound file:", filename
        print "Sample rate:", SAMPLE_RATE
        print "Duration (sec):", DURATION_SEC
        print "# samples:", SAMPLE_LEN
        wavefile = wave.open(filename, 'w')
        wavefile.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
        samples = []
	DEBUG_SAMPLE1,DEBUG_SAMPLE2 = [],[]
        for i in range(SAMPLE_LEN/2):
                t = float(i) / SAMPLE_RATE
                sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi)
		if i > SAMPLE_LEN/2 - 10:
			DEBUG_SAMPLE1.append(sample)
                packed_sample = struct.pack('h', sample)
                samples.append(packed_sample)
	for i in range(SAMPLE_LEN/2,SAMPLE_LEN):
		t = float(i) / SAMPLE_RATE
                sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi + math.pi)
		if i < SAMPLE_LEN/2 + 10:
			DEBUG_SAMPLE2.append(sample)
                packed_sample = struct.pack('h', sample)
                samples.append(packed_sample)
	#print "[DebugInfo]:"
	#print DEBUG_SAMPLE1,DEBUG_SAMPLE2
        sample_str = ''.join(samples)
        wavefile.writeframes(sample_str)
        wavefile.close()
        return filename

'''
Function:PSKSequenceZeroWaveMake(freq,time)
Effect: A complex type of PSK audio signal
说明：该束PSK信号传递的是10 110 1110 11110，规则为经典的PSK模式
Input1: freq : frequency of the required audio file
Input2: time : the time length of the audio file
Output: the filename of the audio file
Version:
0.1     master branch   Author:Luo      Date:11/09
'''
def PSKComplexZeroWaveMake(freq,time):
	MAX_AMPLITUDE = 32767
        SAMPLE_RATE = 44100
        DURATION_SEC = time
        SAMPLE_LEN =  SAMPLE_RATE * DURATION_SEC
        filename = './'+ str(freq) + 'Hz_'+ str(DURATION_SEC) + 's_PSKSequenceZero.wav'
        print "Creating sound file:", filename
        print "Sample rate:", SAMPLE_RATE
        print "Duration (sec):", DURATION_SEC
        print "# samples:", SAMPLE_LEN
        wavefile = wave.open(filename, 'w')
        wavefile.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
        samples , DEBUG_SAMPLES= [], []
        PSK_NUM = SAMPLE_LEN / freq * 2
	PSK_CONVERT = [0]
	temp , flag = 1,0
	while 1:
		flag += temp
		if PSK_NUM * flag < SAMPLE_LEN:
			PSK_CONVERT.append(PSK_NUM * flag)
		else:
			break
		temp += 1 
	PSK_CONVERT.append(SAMPLE_LEN)
	flag = 0
        for i in range(SAMPLE_LEN):
		if i >= PSK_CONVERT[flag] and i < PSK_CONVERT[flag+1] and flag%2==0:
			t = float(i) / SAMPLE_RATE
                	sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi)
		elif i >= PSK_CONVERT[flag] and i < PSK_CONVERT[flag+1] and flag%2==1:
			t = float(i) / SAMPLE_RATE
                        sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi + math.pi)
		elif i == PSK_CONVERT[flag+1]:
			flag += 1
			t = float(i) / SAMPLE_RATE
                        sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi)
		DEBUG_SAMPLES.append(sample)
                packed_sample = struct.pack('h', sample)
                samples.append(packed_sample)
        #print "[DebugInfo]:"
        #print DEBUG_SAMPLES
	#print PSK_CONVERT
        sample_str = ''.join(samples)
        wavefile.writeframes(sample_str)
        wavefile.close()
        return filename



'''
Function:PSKBalanceZeroWaveMake(freq,time)
Effect: A complex type of PSK audio signal
说明：该束PSK信号传递的是110 110 110 110，规则为经典的PSK模式
Input1: freq : frequency of the required audio file
Input2: time : the time length of the audio file
Output: the filename of the audio file
Version:
0.1     master branch   Author:Luo      Date:11/11
'''
def PSKBalanceZeroWaveMake(freq,time):
	MAX_AMPLITUDE = 32767
        SAMPLE_RATE = 44100
        DURATION_SEC = time
        SAMPLE_LEN =  SAMPLE_RATE * DURATION_SEC
        filename = './'+ str(freq) + 'Hz_'+ str(DURATION_SEC) + 's_PSKBalanceZero.wav'
        print "Creating sound file:", filename
        print "Sample rate:", SAMPLE_RATE
        print "Duration (sec):", DURATION_SEC
        print "# samples:", SAMPLE_LEN
        wavefile = wave.open(filename, 'w')
        wavefile.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
        samples , DEBUG_SAMPLES= [], []
        PSK_INTERVAL = SAMPLE_LEN / freq * 60
	PSK_CONVERT = [0]
	flag = 1
	while 1:
		if PSK_INTERVAL * flag < SAMPLE_LEN:
			PSK_CONVERT.append(PSK_INTERVAL * flag)
		else:
			break
		flag += 1 
	PSK_CONVERT.append(SAMPLE_LEN)
	flag = 0
        for i in range(SAMPLE_LEN):
		if i >= PSK_CONVERT[flag] and i < PSK_CONVERT[flag+1] and flag%2==0:
			t = float(i) / SAMPLE_RATE
                	sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi)
		elif i >= PSK_CONVERT[flag] and i < PSK_CONVERT[flag+1] and flag%2==1:
			t = float(i) / SAMPLE_RATE
                        sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi + math.pi)
		elif i == PSK_CONVERT[flag+1]:
			flag += 1
			t = float(i) / SAMPLE_RATE
                        sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi)
		DEBUG_SAMPLES.append(sample)
                packed_sample = struct.pack('h', sample)
                samples.append(packed_sample)
        #print "[DebugInfo]:"
        #print DEBUG_SAMPLES
	#print PSK_CONVERT
        sample_str = ''.join(samples)
        wavefile.writeframes(sample_str)
        wavefile.close()
        return filename

'''
Function:PSKLargeZeroWaveMake(freq,time)
Effect: A complex type of PSK audio signal
说明：该束PSK信号传递的是10 110 1110 11110，但是0之间的间距比较大，规则为经典的PSK模式
Input1: freq : frequency of the required audio file
Input2: time : the time length of the audio file
Output: the filename of the audio file
Version:
0.1     master branch   Author:Luo      Date:11/09
'''
def PSKLargeZeroWaveMake(freq,time):
        MAX_AMPLITUDE = 32767
        SAMPLE_RATE = 44100
        DURATION_SEC = time
        SAMPLE_LEN =  SAMPLE_RATE * DURATION_SEC
        filename = './'+ str(freq) + 'Hz_'+ str(DURATION_SEC) + 's_PSKLargeZero.wav'
        print "Creating sound file:", filename
        print "Sample rate:", SAMPLE_RATE
        print "Duration (sec):", DURATION_SEC
        print "# samples:", SAMPLE_LEN
        wavefile = wave.open(filename, 'w')
        wavefile.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
        samples , DEBUG_SAMPLES= [], []
        PSK_NUM = SAMPLE_LEN / freq * 2
        PSK_CONVERT = [0]
        temp , flag = 1,20
        while 1:
                flag += temp
                if PSK_NUM * flag < SAMPLE_LEN:
                        PSK_CONVERT.append(PSK_NUM * flag)
                else:
                        break
                temp += 5
        PSK_CONVERT.append(SAMPLE_LEN)
        flag = 0
        for i in range(SAMPLE_LEN):
                if i >= PSK_CONVERT[flag] and i < PSK_CONVERT[flag+1] and flag%2==0:
                        t = float(i) / SAMPLE_RATE
                        sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi)
                elif i >= PSK_CONVERT[flag] and i < PSK_CONVERT[flag+1] and flag%2==1:
                        t = float(i) / SAMPLE_RATE
                        sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi + math.pi)
                elif i == PSK_CONVERT[flag+1]:
                        flag += 1
                        t = float(i) / SAMPLE_RATE
                        sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi)
                DEBUG_SAMPLES.append(sample)
		packed_sample = struct.pack('h', sample)
                samples.append(packed_sample)
        #print "[DebugInfo]:"
        #print DEBUG_SAMPLES
        #print PSK_CONVERT
        sample_str = ''.join(samples)
        wavefile.writeframes(sample_str)
        wavefile.close()
        return filename

'''
Function:PSKSequenceZeroTwoPathWaveMake(freq,time)
Effect: A complex type of PSK audio signal. Derived from the PSK sequence zero.
IT is composed of the PSK signals from two paths.
The time difference between two paths is 2 signal period.
Input1: freq : frequency of the required audio file
Input2: time : the time length of the audio file
Output: the filename of the audio file
Version:
0.1     master branch   Author:Luo      Date:11/13
'''
def PSKSequenceZeroTwoPathWaveMake(freq,time):
        MAX_AMPLITUDE = 32767/2
        SAMPLE_RATE = 44100
        DURATION_SEC = time
	TIME_INTERVAL = 2
        VELOCITY = 34300
	SAMPLE_LEN =  SAMPLE_RATE * DURATION_SEC
        filename = './'+ str(freq) + 'Hz_'+ str(DURATION_SEC) + 's_PSKSequenceZeroTwoPath.wav'
        print "Creating sound file:", filename
        print "Sample rate:", SAMPLE_RATE
        print "Duration (sec):", DURATION_SEC
        print "# samples:", SAMPLE_LEN
        wavefile = wave.open(filename, 'w')
        wavefile.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
        samples , DEBUG_SAMPLES= [], []
        PSK_NUM = SAMPLE_LEN / freq * 2
        PSK_CONVERT = [0]
        temp , flag = 1,0
        while 1:
                flag += temp
                if PSK_NUM * flag < SAMPLE_LEN:
                        PSK_CONVERT.append(PSK_NUM * flag)
                else:
                        break
                temp += 1
        PSK_CONVERT.append(SAMPLE_LEN)
        flag = 0
        for i in range(SAMPLE_LEN):
                if i >= PSK_CONVERT[flag] and i < PSK_CONVERT[flag+1] and flag%2==0:
                        t = float(i) / SAMPLE_RATE
                        sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi)
		elif i >= PSK_CONVERT[flag] and i < PSK_CONVERT[flag+1] and flag%2==1:
			t = float(i) / SAMPLE_RATE
                        sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi + math.pi)
		elif i == PSK_CONVERT[flag+1]:
			flag += 1
			t = float(i) / SAMPLE_RATE
                        sample = MAX_AMPLITUDE * math.sin(t * freq * 2 * math.pi)
		samples.append(sample)
	samples_reflected = [0]* int(round(TIME_INTERVAL*SAMPLE_RATE/freq))
	samples_reflected.extend(samples)
	samples_reflected = samples_reflected[:len(samples)]
	for i in range(len(samples)):
		samples[i] = samples[i] + samples_reflected[i]
        
	debuginfo = open("SequenceZeroTwoPath.csv",'w') 
	for i in samples:
		debuginfo.write(str(i)+'\n')
	debuginfo.close()
	
	tmp_samples = []
	for i in range(len(samples)):
		packed_sample = struct.pack('h', samples[i])
        	tmp_samples.append(packed_sample)
	samples = tmp_samples
	
        sample_str = ''.join(samples)
        wavefile.writeframes(sample_str)
        wavefile.close()
        return filename


if __name__ == "__main__":
	
	#PSKSimpleZeroWaveMake(18000,10)
	#Note: 	please use (18000,10x) as the default parameter in this function
	#	Otherwise the PSK convert-phase cannot be guaranteed -- by Shengjie

	#PSKComplexZeroWaveMake(18000,10)
        #Note:  please use (18000,10x) as the default parameter in this function
        #       Otherwise the PSK convert-phase cannot be guaranteed -- by Shengjie

	#PSKBalanceZeroWaveMake(18000,10)
	#PSKLargeZeroWaveMake(18000,10)
	PSKSequenceZeroTwoPathWaveMake(18000,10)
