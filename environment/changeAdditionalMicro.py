import wave
import numpy as np
import sys
import struct

def mainChange(inputname,outputname):
	wave_list=_readwave(inputname)
	_writewave(wave_list,outputname)


def _readwave(inputname):
        wavname = inputname
        wf = wave.open(wavname, "rb")
        nframes = wf.getnframes()
        framerate = wf.getframerate()
        str_data = wf.readframes(nframes)
        wf.close()
        wave_data = np.fromstring(str_data, dtype=np.short)
        wave_data = wave_data.T
        wave_list = wave_data.tolist()
	data1 , data2 = [],[]
	for i in range(len(wave_list)):
		if i % 2 == 0:
			data1.append(wave_list[i])
		else:
			data2.append(wave_list[i])
        return data1

def _writewave(data,outputname):
        SAMPLE_RATE = 44100
        print "Creating sound file:", outputname
        print "Sample rate:", SAMPLE_RATE
        wavefile = wave.open(outputname, 'w')
        wavefile.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
        samples = []
        for i in range(len(data)):
                try:
			sample = data[i]
	                packed_sample = struct.pack('h', sample)
	                samples.append(packed_sample)
		except:
			print data[i]
        sample_str = ''.join(samples)
        wavefile.writeframes(sample_str)
        wavefile.close()

if __name__=="__main__":
	mainChange(sys.argv[1],sys.argv[2])
