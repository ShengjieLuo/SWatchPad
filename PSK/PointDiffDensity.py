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
	threshold = 10
	for i in range(len(zerorange)):
		if zerorange[i][1] - zerorange[i][0] > threshold:
			tmpzerorange.append(zerorange[i])
	zerorange = tmpzerorange
	#print zerorange[:100]

	peakrange = []
	threshold = 10000
	left_limit,right_limit = zerorange[0][0] , zerorange[0][1]
	for i in range(1,len(zerorange)):
		if zerorange[i][1] - left_limit < threshold:
			right_limit = zerorange[i][1]
		else:
			peakrange.append((left_limit,right_limit))
			left_limit,right_limit = zerorange[i][0] , zerorange[i][1]
	#print peakrange

	testrange = []
	tmppeakrange = []
	ideal = 28
	for i in range(1,len(peakrange)):
		interval = (peakrange[i][0] - peakrange[i-1][1])/490
		testrange.append(interval)
		if abs(interval-ideal)<=4:
			tmppeakrange.append(peakrange[i])
	peakrange = tmppeakrange
	print testrange

	result = []
	count = 0
	for limit in peakrange:
		signals = psklist[limit[0]:limit[1]]
		zeros,X = [] , []
		for num in range(len(signals)):
			if signals[num] == 0:
				X.append([num])
				zeros.append(num)	 
		X = np.array(X)
		db = DBSCAN(eps=30,min_samples=10).fit(X)
		#print X
		labels = db.labels_.tolist()
		#print len(labels)
		kind , tmp , typecount = labels[0],[],[]
		first_point , last_point = 0,0
		for i in range(len(labels)):
			if labels[i] != kind and labels[i] != -1:
				last_point = i - 1
				typecount.append(last_point-first_point)
				tmp.append((zeros[last_point] + zeros[first_point])/2)
				first_point = i
				kind = labels[i]
			elif i==len(labels)-1:
				typecount.append(last_point-first_point)
				tmp.append((zeros[i]+zeros[first_point])/2)
		#print zeros
		#print labels
		print limit[0],limit[1],limit[1]-limit[0],tmp
		result.append(tmp[-1]/10)
		#result.append(tmp[typecount.index(max(typecount))]/10)
	return result