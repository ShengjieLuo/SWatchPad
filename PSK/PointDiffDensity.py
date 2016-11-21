import numpy as np
from sklearn.cluster import DBSCAN


def pointdiff(psklist,samplerate,additionalratio,debug=0):
	
	zerorange = []
	i = 0
	while 1:
		if psklist[i]==0:
			flag = 0
			left_limit = i
			i += 1
			while 1:
				try:
					if psklist[i]==0:
						right_limit = i
						i += 1
						flag = 1
					else:
						if flag == 1:
							zerorange.append((left_limit,right_limit))
						break
				except:
					break
		else:
			i += 1
		if i >= len(psklist):
			break
	#print zerorange[:10]

	tmpzerorange = []
	threshold = 5
	for i in range(len(zerorange)):
		if zerorange[i][1] - zerorange[i][0] > threshold:
			tmpzerorange.append(zerorange[i])
	zerorange = tmpzerorange
	#print zerorange[:100]

	peakrange = []
	threshold = 10000
	left_limit,right_limit = zerorange[0][0] , zerorange[0][1]
	for i in range(1,len(zerorange)):
		#if zerorange[i][1] - zerorange[i-1][1] > 1000:
		#	left_limit = zerorange[i][0]	
		if zerorange[i][1] - left_limit < threshold:
			right_limit = zerorange[i][1]
		else:
			peakrange.append((left_limit,right_limit))
			left_limit,right_limit = zerorange[i][0] , zerorange[i][1]
	print peakrange

	testrange = []
	tmppeakrange = []
	ideal = 29
	for i in range(1,len(peakrange)):
		interval = (peakrange[i][0] - peakrange[i-1][0])/490
		testrange.append(interval)
		if abs(interval-ideal)<=4:
			tmppeakrange.append(peakrange[i])
	peakrange = tmppeakrange
	print testrange

	tmppeakrange = []
	for peak in peakrange:
		tmppeakrange.append((peak[1]-1000,peak[1]))
	peakrange = tmppeakrange

	result = []
	count = 0
	for limit in peakrange:
		signals = psklist[limit[0]:limit[1]]
		signals = _filterOutlier(signals)
		zeros,X = [] , []
		for num in range(len(signals)):
			if signals[num] == 0:
				X.append([num])
				zeros.append(num)	 
		X = np.array(X)
		db = DBSCAN(eps=20,min_samples=10).fit(X)
		#print X
		labels = db.labels_.tolist()
		#print len(labels)
		kind ,peaks , typecount = labels[0],[],[]
		first_point , last_point = 0,0
		for i in range(len(labels)):
			if labels[i] != kind and labels[i] != -1:
				last_point = i - 1
				typecount.append(last_point-first_point)
				peaks.append((zeros[last_point] + zeros[first_point])/2)
				first_point = i
				kind = labels[i]
			elif i==len(labels)-1:
				typecount.append(last_point-first_point)
				peaks.append((zeros[i]+zeros[first_point])/2) 
		#print zeros
		#print labels
		print limit[0],limit[1],limit[1]-limit[0],peaks
		result.append(peaks[-1])
		#result.append(tmp[typecount.index(max(typecount))]/10)
	return result

def _filterOutlier(signals):
	result = []
	test = []
	for i in range(0,len(signals),10):
		sample = signals[i:i+10]
		test.append(sum(sample))
		if sum(sample)>= 7:
			sample = [1]*10
		result.extend(sample)
	#print test
	print "zero_singal num: ",len(signals)-sum(result)
	return result
