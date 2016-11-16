


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
		if zerorange[i][1] - zerorange[i][0] > 5:
			tmpzerorange.append(zerorange[i])
	zerorange = tmpzerorange
	#print zerorange[:100]

	peakrange = []
	threshold = 10000
	left_limit,right_limit = zerorange[0][0] , zerorange[0][1]
	for i in range(1,len(zerorange)):
		if zerorange[i][1] - left_limit < 10000:
			right_limit = zerorange[i][1]
		else:
			peakrange.append((left_limit,right_limit))
			left_limit,right_limit = zerorange[i][0] , zerorange[i][1]
	#print peakrange

	testrange = []
	for i in range(1,len(peakrange)):
		interval = (peakrange[i][0] - peakrange[i-1][1])/490
		testrange.append(interval)
	#print testrange

	'''
	disrange = []
	interval = 10
	for i in range(peakrange[0][0]-1000,peakrange[0][1]+1000,interval):
		psksum = sum(psklist[i:(i+interval)])
		if psksum >= 7:
			psksum = 10
		else:
			pass
		disrange.append(psksum)
	prit disrange
	'''
	result = []
	for i in range(len(peakrange)):
		j = peakrange[i][0]
        	onerange = []
		while 1:
                	if sum(psklist[j:j+10])>=7:
                        	flag = 0
	                        left_limit = j
        	                j += 1
                	        while 1:
                        	        try:
                                	        if sum(psklist[j:j+10])>=8:
                                        	        right_limit = j
                                                	j += 1
	                                                flag = 1
							if j >= peakrange[i][1]:
								break
        	                                else:
                	                                if flag == 1:
                        	                                onerange.append((left_limit,right_limit+9))
                                	                break
	                                except:
        	                                break
                	else:
                        	j += 1
	                if j >= peakrange[i][1]:
        	                break
		oneMax = 0
		#if i == 1:
		#	print onerange
		for k in onerange:
			tmp = k[1] - k[0]			
			if tmp<200 and tmp>oneMax:
			#if tmp>oneMax:
				oneMax = tmp
		result.append(oneMax)
	if debug==1:
		print "  [Debug]  The range between neighbor peaks: ",testrange
		print "  [Debug]  The sample point difference list: ",result
		print "  [Debug]  The final sample point difference: ",sum(result)/len(result)
	return sum(result)/len(result)
	'''
        peakrange = []
        threshold ,i= 4000,0
        while 1:
		left_limit = zerorange[i][0]
		while 1:
			try:
				if zerorange[i+1][0] - zerorange[i][0] <= threshold:
					right_limit = zerorange[i+1][1]
					i += 1
					if i == len(zerorange) -1:
						peakrange.append((left_limit,right_limit))
						print peakrange
						break
				else:
					peakrange.append((left_limit,right_limit))
					break
			except:
				break
		if i >= len(zerorange)-1:
                        break
	print peakrange
	'''

if __name__=='__main__':
	pointdiff([1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,01,1,0,0,1,1,0,0,0,0,1,1],44100,10,0)
