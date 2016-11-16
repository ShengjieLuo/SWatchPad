
def waveFreqShift(freq_list,energy_list,peakRef,scanWindow,peakWindow,debug=0):
	peak = wavePeak(freq_list,energy_list,scanWindow,debug)
	peak_around = wavePeakAround(freq_list,energy_list,peak[0],peakWindow,debug)
	freq_shift = weightAveragePeak(peak_around,peak,peakRef,debug)
	return freq_shift

def wavePeak(freq_list,energy_list,FREQ_WINDOW_SIZE,debug):
        peak_flag = 1
        max_energy, max_energy, max_index = 0,0,0
        for i in range(len(energy_list)):
                for k in range(max([i-FREQ_WINDOW_SIZE,0]),min([i+FREQ_WINDOW_SIZE,len(energy_list)-1])):
                        if energy_list[i]<energy_list[k]:
                                peak_flag = 0
                                break
                if peak_flag==1 and energy_list[i]>max_energy:
                        max_energy=energy_list[i]
                        max_freq = freq_list[i]
                        max_index = i
                peak_flag = 1
        return [max_index,max_freq,max_energy]

  
def wavePeakAround(freq_list,energy_list,PEAK_INDEX,AROUND_WINDOW,debug):
        PEAK_AROUND = []
        for i in range(PEAK_INDEX-AROUND_WINDOW,PEAK_INDEX+AROUND_WINDOW):
                PEAK_AROUND.append([i,freq_list[i],energy_list[i]])
        return PEAK_AROUND

 
def weightAveragePeak(PEAK_AROUND,PEAK,PEAK_REF,debug):
	total1 , sum1 = 0.0 ,0.0
	for j in range(1,len(PEAK_AROUND)-1):
		if (PEAK_AROUND[j][2]>PEAK_AROUND[j-1][2]) and (PEAK_AROUND[j][2] > PEAK_AROUND[j+1][2]) and (PEAK_AROUND[j][2] > PEAK[2]*0.3):
			total1 += PEAK_AROUND[j][2] * PEAK_AROUND[j][1]
			sum1 += PEAK_AROUND[j][2]
			if debug == 1:
				print "  [Debug]  PEAK_AROUND: ",PEAK_AROUND[j][2],PEAK_AROUND[j][1]
	freq1 = total1/sum1-PEAK_REF
	if debug == 1:
		print "  [Debug]  Weight Average Frequency Shift: "+str(freq1)
	result = freq1
	return result

