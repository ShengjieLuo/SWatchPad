from ffthann import ffttran as _fft


def dopplerMain(wavfile):
	leftlimit = 16000
	rightlimit = 18000
	x_data , y_data = _fft(wavfile,leftlimit,rightlimit)

def analysisInfo(flag=1):
        # flag = 0 : initial state
        # flag = 1 : test state
        for i in FREQ_LIST:
                peak1,peak2 = wavePeakIndex(i,FREQ_WINDOW_SIZE)
                peak1Around,peak2Around = wavePeakAround(i,peak1,peak2,ANALYSIS_AROUND_WINDOW)
                ANALYSIS_PEAK.append([peak1,peak2])
                ANALYSIS_AROUND.append([peak1Around,peak2Around])
                print [peak1,peak2]
                return 0
        ANALYSIS_PEAK_REF = loadPeak(INITIAL_FILE[2])
        RECORD_SECONDS_NUM = int(RECORD_SECONDS_TOTAL / RECORD_SECONDS_UNIT - FREQ_RECORD_INTERVAL )
        printPeakAround(ANALYSIS_AROUND,ANALYSIS_AROUND_FILE,RECORD_SECONDS_NUM)
        ANALYSIS_AROUND_ITP = valueInterpolate(ANALYSIS_AROUND,RECORD_SECONDS_NUM)
        printPeakAround(ANALYSIS_AROUND_ITP,ANALYSIS_ITP_FILE,RECORD_SECONDS_NUM)
        #WeightAveragePeak(ANALYSIS_AROUND_ITP,ANALYSIS_WEIGHT_FILE,RECORD_SECONDS_NUM,ANALYSIS_PEAK_REF)
        ANALYSIS_RESULT = weightAveragePeak(ANALYSIS_AROUND_ITP,ANALYSIS_WEIGHT_FILE,RECORD_SECONDS_NUM,ANALYSIS_PEAK_REF,ANALYSIS_PEAK)
        return ANALYSIS_RESULT

