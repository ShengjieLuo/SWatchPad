import difflib

def firstpeak(wavlist,psklist,samplerate,additionalratio,debug):
	refname = "nohandmode.txt"
	zerolist,zerodist = _scan(wavlist,debug)
	refdist 	= _ref(samplerate,additionalratio,debug)
	outlier 	= _detect(zerolist,zerodist,refdist,debug)
	iphase		= _range(outlier,debug) 
	#ipsk		= _psk(iphase,psklist)
	ipsk		= _strpsk(iphase,psklist,debug)
	refmode		= _readmode(refname,debug)
	result		= _compare(ipsk,refmode,debug)
	#_initial_test(ipsk,debug)
	return result

def _scan(wavlist,debug):
	zerolist = []
	for i in range(1,len(wavlist)):
		if wavlist[i]*wavlist[i-1]<0:
			zerolist.append(i)
	zerodistance = []
	for i in range(0,len(zerolist)-1):
		zerodistance.append(zerolist[i+1]-zerolist[i])
	'''
	if debug==1:
		print "  [Debug]  The zero distance: ",zerodistance[:100]
	'''
	return zerolist,zerodistance

def _ref(rate,ratio,debug):
	return int(round((rate+0.0)*ratio/18000/2))

def _detect(zerolist,zerodist,refdist,debug):
	outlier = []
	for i in range(len(zerodist)):
		if abs(zerodist[i]- refdist) > 5:
			outlier.append((zerolist[i],zerodist[i]))
	if debug==1:
		print "  [Debug]  The outliers: "
		for i in range(10):
			print "  Num:"+str(i)+" "+str(outlier[i][0])+" Period Length:"+str(outlier[i][1])
	return outlier

def _range(outlier,debug):
	iphase = []
	leftlimit , rightlimit = outlier[0][0] , sum(outlier[0])
	for i in range(0,len(outlier)-1):
		if abs(outlier[i+1][0]-outlier[i][0])<150:
			rightlimit = outlier[i+1][0] + outlier[i+1][1]
		else:
			iphase.append((leftlimit,rightlimit))
			leftlimit , rightlimit = outlier[i+1][0] , sum(outlier[i+1])
	iphase.append((leftlimit,rightlimit))
	for i in range(len(iphase)-1,-1,-1):
		if iphase[i][1] - iphase[i][0] < 150:
			iphase.remove(iphase[i])
	if debug==1:
		print "  [Debug]  The inverse phase field: ",iphase[:10]
	return iphase

def _psk(iphase,psklist,debug):
	ipsk = []
	for i in range(iphase):
		ipsk.append(psklist[iphase[i][0]:iphase[i][1]])
	return ipsk

def _strpsk(iphase,psklist,debug):
        ipsk = []
        for i in range(len(iphase)):
		tmp = ""
		for k in range(iphase[i][0],iphase[i][1]):
			tmp = tmp + str(psklist[k])
		ipsk.append(tmp)
        return ipsk

'''
def _difflib_leven(str1, str2,debug):
	leven_cost = 0
	s = difflib.SequenceMatcher(None, str1, str2)
	for tag, i1, i2, j1, j2 in s.get_opcodes():
		if tag == 'replace':
			leven_cost += max(i2-i1, j2-j1)
		elif tag == 'insert':
			leven_cost += (j2-j1)
		elif tag == 'delete':
			leven_cost += (i2-i1)
	return leven_cost
'''

def _difflib_leven(str1, str2,debug):
	s1 , s2 = str1 , str2
	m, n = len(s1), len(s2)
	colsize, matrix = m + 1, []
	for i in range((m + 1) * (n + 1)):
		matrix.append(0)
	for i in range(colsize):
		matrix[i] = i
	for i in range(n + 1):
		matrix[i * colsize] = i
	for i in range(n + 1)[1:n + 1]:
		for j in range(m + 1)[1:m + 1]:
			cost = 0
        		if s1[j - 1] == s2[i - 1]:
	            		cost = 0
		        else:
            			cost = 1
		        minValue = matrix[(i - 1) * colsize + j] + 1
		        if minValue > matrix[i * colsize + j - 1] + 1:
				minValue = matrix[i * colsize + j - 1] + 1
		        if minValue > matrix[(i - 1) * colsize + j - 1] + cost:
			        minValue = matrix[(i - 1) * colsize + j - 1] + cost
		        matrix[i * colsize + j] = minValue
	return matrix[n * colsize + m]

'''
def _initial_test(ipsk,debug):
	fp = open("nohangmode.txt",'a')
	fp.write(ipsk[0]+'\n')
	fp.write(ipsk[2]+'\n')
	fp.close()	
'''

def _readmode(filename,debug):
	fp = open(filename,'r')
	modelist = [] 
	for line in fp.readlines():
		line = line.strip()
		modelist.append(line)
	#print modelist
	return modelist

def _regioncompare(str1,str2,debug):
	step = 1
	window = 25
	threshold = 17
	comparelist = []
	for  i in range(0,min([len(str1),len(str2)])-window,step):
		str1region = str1[i:i+window]
		str2region = str2[i:i+window]
		compare = _difflib_leven(str1region,str2region,debug)
		comparelist.append(compare)
	result = comparelist.index(max(comparelist[:150]))
	flag = sum(comparelist[:50])	
	#print compare
	return result,flag
	

def _compare(ipsk,modelist,debug):
	resultlist = []
	zerofirstMode = modelist[0]
	onefirstMode = modelist[1]
	_compareshow(ipsk[3],zerofirstMode,onefirstMode,debug)
	for string in ipsk:
		result1 , flag1 = _regioncompare(string,zerofirstMode,debug)
		result2 , flag2 = _regioncompare(string,onefirstMode,debug)	
		'''
		#Judge Method 1
		if flag1>flag2:
			result = result2
		else:
			result = result1
		'''
		#Judge Method 2
		#'''
		if string[:3] == "000":
			result = result1
		elif string[:3] == "111":
			result = result2
		else:
			result = -1
		#'''
		resultlist.append(result)
	print resultlist
	return resultlist
		
def _compareshow(str1,str2a,str2b,debug):
	step = 1
        window = 25
        comparelist = []
	for  i in range(0,min([len(str1),len(str2a)])-window,step):
		str1region = str1[i:i+window]
                str2region = str2a[i:i+window]
                compare = _difflib_leven(str1region,str2region,debug)
		comparelist.append(compare)
	print comparelist
	comparelist = []
	for  i in range(0,min([len(str1),len(str2b)])-window,step):
                str1region = str1[i:i+window]
                str2region = str2b[i:i+window]
                compare = _difflib_leven(str1region,str2region,debug)
                comparelist.append(compare)
        print comparelist
	
