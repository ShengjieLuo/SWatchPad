
def firstpeak(wavlist,samplerate,additionalratio,debug):
	zerolist,zerodist = _scan(wavlist,debug)
	refdist = _ref(samplerate,additionalratio,debug)
	outlier = _detect(zerolist,zerodist,refdist,debug)
	return outlier

def _scan(wavlist,debug):
	zerolist = []
	for i in range(1,len(wavlist)):
		if wavlist[i]*wavlist[i-1]<0:
			zerolist.append(i)
	zerodistance = []
	for i in range(1,len(zerolist)):
		zerodistance.append(zerolist[i]-zerolist[i-1])
	if debug==1:
		print "  [Debug]  The zero distance: ",zerodistance[:100]
	return zerolist,zerodistance

def _ref(rate,ratio,debug):
	return int(round((rate+0.0)*ratio/18000/2))

def _detect(zerolist,zerodist,refdist,debug):
	outlier = []
	for i in range(len(zerodist)):
		if abs(zerodist[i]- refdist) > 5:
			outlier.append(zerolist[i+1])
	if debug==1:
		print "  [Debug]  The outliers: ",outlier[:100]
	return outlier
