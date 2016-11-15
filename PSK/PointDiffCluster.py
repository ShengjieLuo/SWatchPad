#coding:utf-8

'''
Function: _pointdiff()
input:	psklist		the data structure of the PSK digital signal
input:	debug		debug flag. If debug = 1,verbose the debug infomation
output:	diff		the point difference of signals from two path
'''
from sklearn.cluster import KMeans

def _pointdiff(psklist,samplerate,additionalratio,debug=0):
	
	
	#******************************************************************
	# Step 0 : Print original infomation                              *
	# 1. Count the zero number in the signal list			  *
	#******************************************************************
	zero_count0 = 0
	for i in range(len(psklist)):
		if psklist[i]==0:
			zero_count0 += 1
		
	#******************************************************************
	# Step 1 : Locate the continuous zero signal                      *
	# 1. Locate the continuous zero signal, the number of  continuous *
	#    signal numbers should be larger than 2*num 		  *
	# 2. Record the left_limit and right_limit of the continuous	  *
	#    zero signals, we call it zerorange.			  *
	#******************************************************************
	psklist1 , zerorange = [],[]
	num = 10
	zero_count1 = 0
	left_limit,right_limit = -1,-1
	for i in range(1,len(psklist)):
		flag = 0	
		for j in psklist[i-num:i+num]:
			if j==1:
				flag = 1
				break
		if flag == 0:
			if left_limit <= i and right_limit >= i:
				continue
			left_limit,right_limit = i,i
			while 1:
				left_limit -= 1
				try:
					if psklist[left_limit] == 1:
						break
					else:
						continue
				except:
					break
			while 1:
				right_limit += 1
				try:
					if psklist[right_limit] == 1:
						break
					else:
						continue
				except:
					break
			zerorange.append((left_limit,right_limit))
	tmpzerorange=list(set(zerorange))
	tmpzerorange.sort(key=zerorange.index)	
	
	
	#******************************************************************
	# Step 2: improve the zero signal                                 *
	# 1. Merge the neighbor zero ranges into one zero range.          *
	#    if points between two zero ranges are fewer than threshold,  *
	#    we would merge them and regard the gap as an outlier         *
	#******************************************************************
	zerorange = tmpzerorange
	tmpzerorange = []
	threshold = 25
	i ,overlap = 0,0
	while 1:
		flag = 0
		if zerorange[i+1][0] - zerorange[i][1]<threshold:
			tmpzerorange.append((zerorange[i][0],zerorange[i+1][1]))
			overlap,flag = 1,1
			i += 1
		else:
			tmpzerorange.append(zerorange[i])
		i += 1
		if i >= len(zerorange) - 1:
			if flag == 0:
				tmpzerorange.append(zerorange[i])
			i = 0
			zerorange = tmpzerorange
			tmpzerorange = []
			if overlap == 0:
				break
			else:
				overlap = 0
	'''
	tmpzerorange = []
	i = 0
	while 1:
		if zerorange[i][1] >= zerorange[i+1][1]:
			tmpzerorange.append(zerorange[i])
			i += 1
		else:	
			tmpzerorange.append(zerorange[i])
		i += 1
		#print i,len(zerorange)
		if i >= len(zerorange)-1:
			break
	zerorange = tmpzerorange
	'''
	#******************************************************************
	



	#******************************************************************
	# Step 3: Cluster in zerorange                                    *
	# 1. Change the zerorange info into the point difference between  *
	#    two ranges. For example, range (0,7) and (10,17) --> 3       *
	# 2. Clustering the zerodiff to find the major feature            *
	#******************************************************************
	zerodiffs = []
	REF_FREQ = 18000
	CLUSTER_NUM = 50
	POINT_PER_PERIOD = int(round(samplerate * additionalratio / REF_FREQ))
	for i in range(len(zerorange)-1):
		zerodiff = zerorange[i+1][0]-zerorange[i][1]
		if zerodiff < 0:
			zerodiff = POINT_PER_PERIOD + zerodiff
		zerodiffs.append(zerodiff)
	clustertmp = []
	for i in zerodiffs:
		clustertmp.append([float(i)])
	clf = KMeans(CLUSTER_NUM)
	s = clf.fit(clustertmp)
	clusterGroup = clf.cluster_centers_
	clusterLabel = clf.labels_
	clusterCount = [0] * CLUSTER_NUM
	for i in clusterLabel:
		clusterCount[i] = clusterCount[i] + 1
	clusterCandidate = []
	for i in range(len(clusterCount)):
		if clusterCount[i]>sum(clusterCount)/10  and clusterGroup[i][0]<300:
			clusterCandidate.append(clusterGroup[i][0])
	clusterMax = max(clusterCandidate)
	diff = clusterMax
	
	#******************************************************************
	# DEBUG_INFO                                                      *
	#******************************************************************
	if debug == 1:
		print "  [Debug]  The original zero signal: ",zero_count0
		print "  [Debug]  The zero signal after filtering: ",len(zerorange)
		print "  [Debug]  The zero range: ",zerorange
		print "  [Debug]  The difference between two ranges: ",zerodiffs
		print "  [Debug]  The center of the difference group: "
		string = ""
		for i in clusterGroup:
			string = string + str(int(i[0]))+' '
		print string + '\n'
		print "  [Debug]  The distribution of the cluster group: ",clusterCount
		print "  [Debug]  The candidate of the final difference: ",clusterCandidate
		print "  [Debug]  The point difference between two paths: ",diff
	
	return diff
