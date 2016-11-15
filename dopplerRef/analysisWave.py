'''
def wavePeakIndex(FREQ_DATA,FREQ_WINDOW_SIZE):
	peak_flag = 1
	energy_list = FREQ_DATA[1]
	freq_list = FREQ_DATA[0]
	max_energy1,max_energy2 = 0,0
	max_freq1,max_freq2 = 0,0
	max_index1,max_index2 = 0,0
	#low_frequency,high_frequency = 16000,17000
	for i in range(len(energy_list)): 
		for k in range(max([i-FREQ_WINDOW_SIZE,0]),min([i+FREQ_WINDOW_SIZE,len(energy_list)-1])):
			if energy_list[i]<energy_list[k]:
				peak_flag = 0
				break
		if peak_flag==1 and energy_list[i]>max_energy1:
			if energy_list[i] > max_energy2:
				max_energy1 = max_energy2
				max_freq1 = max_freq2
				max_index1 = max_index2		
				max_energy2 = energy_list[i]
				max_freq2 = freq_list[i]
				max_index2 = i
			elif max_energy1 < energy_list[i] and energy_list[i] <= max_energy2:
				max_energy1=energy_list[i]
				max_freq1 = freq_list[i]
				max_index1 = i		
		peak_flag = 1
	if max_index1<max_index2:
		return [max_index1,max_freq1,max_energy1],[max_index2,max_freq2,max_energy2]
	elif max_index2<max_index1:
		return [max_index2,max_freq2,max_energy2],[max_index1,max_freq1,max_energy1]
'''

def wavePeakIndex(FREQ_DATA,FREQ_WINDOW_SIZE):
	peak_flag = 1
	energy_list = FREQ_DATA[1]
	freq_list = FREQ_DATA[0]
	max_energy1,max_energy2 = 0,0
	max_freq1,max_freq2 = 0,0
	max_index1,max_index2 = 0,0
	low_frequency,high_frequency = 16000,17000
	for i in range(len(energy_list)): 
		for k in range(max([i-FREQ_WINDOW_SIZE,0]),min([i+FREQ_WINDOW_SIZE,len(energy_list)-1])):
			if energy_list[i]<energy_list[k]:
				peak_flag = 0
				break
		if peak_flag==1 and energy_list[i]>max_energy1 and freq_list[i]<(low_frequency+high_frequency)/2.0:
			max_energy1=energy_list[i]
			max_freq1 = freq_list[i]
			max_index1 = i
		elif peak_flag==1 and energy_list[i]>max_energy2 and freq_list[i]>(low_frequency+high_frequency)/2.0:		
			max_energy2 =energy_list[i]
			max_freq2 = freq_list[i]
			max_index2 = i
		peak_flag = 1
	return [max_index1,max_freq1,max_energy1],[max_index2,max_freq2,max_energy2]


def waveStatic(peak1Info,peak2Info,stat):
	stat = waveStatic1Info(peak1Info,peak2Info,stat)
	result = waveStatic1Display(stat)
	return result

def waveStatic1Display(stat):
	result = []
	for i in stat:
		if i[2]>0:
			result.append("far")
		elif i[2] == 0:
			result.append("static")
		else:
			result.append("near")
		result.append(i[3])
	return result

def waveStatic1Info(peak1,peak2,stat):
	stat1 = waveStatic1Peak(peak1,0,stat)
	stat2 = waveStatic1Peak(peak2,1,stat)
	stat = []
	stat.append(stat1)
	stat.append(stat2)

def waveStatic1Info(peak1,peak2,stat):
	stat1 = waveStaticPeak(peak1,0,stat)
	stat2 = waveStaticPeak(peak2,1,stat)
	stat = []
	stat.append(stat1)
	stat.append(stat2)
	return stat

def waveStaticPeak(peak,peakNum,stat):
	left1,right1 = waveStatic1PeakAround(peak,1)
	flag = left1/right1 / (stat[peakNum][0]/stat[peakNum][1])
	if flag>1:
		return left1,right1,1,flag
	elif flag==1:
		return left1,right1,0,flag
	else:
		return left1,right1,-1,flag
	
def waveStaticPeakAround(peak,n):
	left = energyData[-1][peak[0]-n]/energyData[-1][peak[0]]
	right = energyData[-1][peak[0]+n]/energyData[-1][peak[0]]
	return left,right

