import wave
import pyaudio
import math
import struct

def waveMake(freq1,freq2,time):
	MAX_AMPLITUDE = 32767
	SAMPLE_RATE = 44100 
	DURATION_SEC = 	time
	SAMPLE_LEN = SAMPLE_RATE * DURATION_SEC
	filename = './'+ str(freq1) + 'Hz_' + str(freq2)+ 'Hz_'+ str(DURATION_SEC) + 's.wav'
	print "Creating sound file:", filename
	print "Sample rate:", SAMPLE_RATE
	print "Duration (sec):", DURATION_SEC
	print "# samples:", SAMPLE_LEN
	wavefile = wave.open(filename, 'w') 
	wavefile.setparams((2, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed')) 
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

if __name__ == "__main__":
	waveMake(16000,16995,60)
