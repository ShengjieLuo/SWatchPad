
def pointDiff(psklist,samplerate,additionalratio,debug=0):
	FIRST_WINDOW = 25
	FIRST_STEP = 10	
	FIRST_THRESHOLD = 10
	zeroBeginList = _firstLevelSearch(psklist,FIRST_WINDOW,FIRST_STEP,FIRST_THRESHOLD)
	zeroBeginList = _firstLevelConnect(zeroBeginList,FIRST_WINDOW,FIRST_STEP)
	zeroField = _firstLevelField(zeroBeginList)
	_firstLevelTest(zeroField)
	#print _firstLevelSample(psklist,zeroField,1)
	samplelist = _secondLevelFilter(psklist,zeroField)
	regionlist = _secondLevelRegionZero(samplelist)
	return [100,1000]

def _firstLevelSearch(psklist,window,step,thre):
	result = []
	for i in range(window,len(psklist),step):
		if sum(psklist[i-window:i]) < thre:
			result.append(i-window)
	print result[:100]
	return result

def _firstLevelConnect(zerolist,window,step):
	result = []
	count = 1
	leftlimit = zerolist[0]
	while count<len(zerolist):
		while 1:
			if zerolist[count]-zerolist[count-1]==step:
				#rightlimit = zerolist[count]+window
				count += 1
			else:
				rightlimit = zerolist[count-1]
				result.append((leftlimit,rightlimit))
				leftlimit = zerolist[count]
				break
			if count>=len(zerolist)-1:
				break
		count += 1
	print result[:10]
	return result

def _firstLevelField(zerolist):
	peakrange = []
        threshold = 1000
        left_limit,right_limit = zerolist[0][0] , zerolist[0][1]
        for i in range(1,len(zerolist)):
                if zerolist[i][1] - right_limit < threshold:
                        right_limit = zerolist[i][1]
                else:
                        peakrange.append((left_limit,right_limit))
                        left_limit,right_limit = zerolist[i][0] , zerolist[i][1]
        print peakrange[0:10]
	return peakrange

def _firstLevelTest(peakrange):
	testrange = []
	for i in range(1,len(peakrange)):
                interval = (peakrange[i][0] - peakrange[i-1][0])/490
                testrange.append(interval)
        print testrange


def _firstLevelSample(psklist,peakrange,num):
	return psklist[peakrange[num][0]:peakrange[num][1]]


def _secondLevelFilter(psklist,peakrange):
	samplelist = []
	for num in range(len(peakrange)):
		psksample= _firstLevelSample(psklist,peakrange,num)
		for i in range(5,len(psksample)):
			if psksample[i:i+5] == [0]*5:
				break
		psksample = psksample[i:]
		samplelist.append(psksample)
	#print samplelist[0]
	print psklist[peakrange[0][0]-100:peakrange[0][1]+100]
	return samplelist

def _secondLevelRegionZero(samplelist):
	regionlist = []
	tmplist = []
	for sample in samplelist:
		for i in range(10,len(sample),10):
			tmplist.append(sum(sample[:i]))
		regionlist.append(tmplist)
		tmplist = []
	print regionlist[0]
	return regionlist	 
