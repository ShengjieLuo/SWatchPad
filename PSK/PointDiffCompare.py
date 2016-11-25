import difflib
import numpy as np
from sklearn.cluster import DBSCAN

def pointDiff(wavlist,psklist,samplerate,additionalratio,debug):
	refname = "nohandmode.txt"
	zerolist,zerodist = _scan(wavlist,debug)
	refdist 	= _ref(samplerate,additionalratio,debug)
	outlier 	= _detect(zerolist,zerodist,refdist,debug)
	iphase		= _range(outlier,debug) 
	#ipsk		= _psk(iphase,psklist)
	ipsk		= _strpsk(iphase,psklist,debug)
	refmode		= _readmode(refname,debug)
	result		= _compare(ipsk,refmode,debug)
	final		= _regulate(result,debug)
	#_initial_test(ipsk,debug)
	return final

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
		print "  [Debug]  The inverse phase field: ",iphase[:100]
	'''
	for i in range(len(iphase)-1,0,-1):
		if iphase[i][1] - iphase[i-1][1] < 10000:
			iphase.remove(iphase[i])
	'''
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
	#_compareshow(ipsk[3],zerofirstMode,onefirstMode,debug)
	for string in ipsk:
		result1 , flag1 = _regioncompare(string,zerofirstMode,debug)
		result2 , flag2 = _regioncompare(string,onefirstMode,debug)	
		
		#Judge Method 1
		#'''
		if flag1>flag2:
			result = result2
		else:
			result = result1
		if result<140 and result!=0:
			resultlist.append(result)
		else:
			resultlist.append(-1)
		#'''
		
		#Judge Method 2
		'''
		if string[:3] == "000":
			result = result1
		elif string[:3] == "111":
			result = result2
		else:
			result = -1
		resultlist.append(result)
		'''
	if debug==1:
		print "  [Debug]  The original result list:  ",resultlist
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

def _regulate(result,debug):
	step = 1
	window = 10
	finals = []
	for i in range(0,len(result)-window,step):
		region = result[i:i+window]
		while -1 in region:
			region.remove(-1)
		final = _cluster(region,debug)
		finals.append(final)
	if debug == 1:
		print "  [Debug]  The final point difference: ",finals
	return finals	

def _cluster(signals,debug):
	X = []
	for signal in signals:
		X.append([signal])
	X = np.array(X)
	db = DBSCAN(eps=15,min_samples=3).fit(X)
	labels = db.labels_.tolist()
	typearray , labelarray = [0]*10, []
	for i in range(10):
		labelarray.append([])
	for i in range(len(labels)):
		typearray[int(labels[i])] += 1
		labelarray[int(labels[i])].append(signals[i])
	maxtype = typearray.index(max(typearray))
	points = labelarray[maxtype]
	result = int((sum(points)+0.0)/len(points))
	'''
	if debug == 1:
		print "  [Debug]  The label situation: ",labelarray
	'''
	return result

if __name__ == '__main__':
	#Here is the sample of a hand-high test audio. We use it to testify our system.
	sample = [92, 114, 120, 55, 96, 115, 92, 123, 55, 19, 112, 80, 130, 112, 108, -1, 80, 92, 97, 121, 8, 69, 112, 44, 121, 136, -1, 138, 119, 136, 80, 121, 93, -1, 121, 61, 124, 121, 120, 112, -1, 112, -1, 103, 127, 112, 112, 108, 112, 61, 52, 112, 39, 121, -1, 123, 121, -1, 19, 69, 128, 76, -1, -1, 120, 114, 110, 60, 52, 61, 112, 55, 121, 123, 123, 92, 123, 112, 121, 125, 120, -1, 10, -1, 53, 96, 95, 53, 96, 97, 107, 53, 120, 87, 107, 65, 96, 107, 120, 10, 128, 94, 108, 44, 96, 59, -1, -1, 92, 120, -1, 54, 128, 52, 55, 44, 126, 53, 128, 118, 109, 120, -1, 92, 121, 132, 128, 74, 112, 121, 121, -1, 128, 127, 65, 117, 105, 109, 94, 92, 112, 71, 129, 66, 121, 112, 112, 121, 112, 87, 120, 60, -1, 120, 121, 112, 121, 126, 121, 62, 137, 117, 120, 112, 112, 122, 92, 138, 121, 124, 112, 121, 121, 120, 120, 121, 126, 108, 121, 112, 111, 121, 112, 120, 110, 68, 121, 118, 97, 92, 121, 120, 112, 110, 121, 121, 112, 129, 109, -1, 112, 118, 121, 138, 119, 121, 123, 121, 110, 112, 125, 112, 112, 120, 124, 120, 114, 121, 121, 120, 120, 128, 124, -1, 121, 117, 128, 112, 112, 121, 121, -1, 112, 72, 121, 92, -1, -1, 118, 121, 119, -1, 119, 123, -1, 112, 95, 121, 119, 121, 121, 112, 126, 121, 121, 67, 126, -1, -1, 112, 112, 112, 121, 112, 123, 112, 112, 22, 97, 2, 125, 111, 112, 111, 120, 124, 126, 121, 121, 90, 121, 110, 123, 119, 120, 92, 128, 44, 74, 122, 112, 112, 112, 121, 120, 118, 126, 119, 117, 121, 96, 108, 121, 138, 112, 112, 121, 123, 112, 112, 73, 112, 112, 121, 121, 126, 124, 52, 55, 119, 112, 121, 112, 126, 112, 112, 112, 128, 121, 112, 114, 112, 129, 121, 120, 112, 129, 129, 121, 121, 107, 124, 112, 80, 121, -1, 122, 133, 124, 112, 117, 121, 126, 121, 120, 117, 126, 129, 124, 129, 109, 112, 119, 115, 112, -1, 121, 112, -1, 112, 129, 112, 116, 121, 119, 121, 121, 111, 126, 121, 97, 112, 116, 121, 126, 120, 120, 119, -1, 121, 119, 121, 121, 121, 125, 126, 113, 55, 55, 111, -1, 63, 120, 129, 111, 112, 128, 74, 112, 115, 112, 121, -1, 125, 121, 120, -1, 116, 112, 112, 121, 121, 121, 121, 118, 112, 129, 112, 121, 112, 108, 131, -1, -1, 112, 121, 125, 120, 121, 121, 139, 120, 112, 138, 129, 112, 121, 121, 73, 117, 120, 129, 121, 119, 105, 94, 97, 125, 112, 111, 2, 106, 53, 121, 111, 112, 119, 120, 52, 121, -1, 92, 121, 112, 67, 121, 120, -1, 138, 53, 95, 84, 133, 97, 125, 5, 117, 119, 105, 107, 72, 121, 138, 97, 125, 84, -1, 120, 67, 94, 91, 3, -1, 124, -1, 36, 124, 125, 121, 97, 97, 129, 120, 121, 121, 112, 80, 107, 119, 120, 119, 95, 90, 61, 124, 71, 121, 121, 87, 127, 111, 112, 121, 112, 124, 121, 95, 126, 121, 121, 112, 112, 127, 121, -1, 72, 105, 125, 126, 112, 121, -1, 112, 120, 112, 111, 87, 139, 124, 121, 122, 114, 112, -1, 96, 107, 121, 112, 110, -1, 55, 42, 90, 96, 112, 117, 126, 121, 112, 38, 112, 112, 112, 121, 126, 112, -1, 127, 120, 123, 99, 121, 121, 65, 123, 108, 95, 126, 116, 125, 112, 129, 120, 121, 112, 63, 132, 120, 121, -1, 124, 63, 55, 73, 121, 121, 111, 112, 129, -1, 112, 126, 121, 110, 72, -1, 114, 2, 121, 104, 126, 112, 127, 118, 115, 126, 121, 118, 112, 112, 112, 115, 121, 121, 67, 112, -1, 121, 121, 125, 128, 126, 124, 97, -1, 63, 128, 67, 112, 129, 109, 123, 112, -1, 120, 126, 105, 121, -1, 121, 112, 121, -1, 112, 67, 112, 121, 112, 125, 128, 110, 112, 121, 126, 121, 72, -1]
	_regulate(sample,1)
