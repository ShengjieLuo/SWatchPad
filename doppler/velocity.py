

def VelocityCal(shift1,shift2,reffreq,x,y):
	deltaD1 = _getVelocity(shift1,reffreq)
	deltaD2 = _getVelocity(shift2,reffreq)
	l1 = 2.10
	l2 = 11.95
	return [_getVx(l1,l2,x,y,deltaD1,deltaD2),_getVy(l1,l2,x,y,deltaD1,deltaD2)]

def _getVelocity(shift,reffreq):
	return (shift+0.0)*34300/reffreq

def _getVx(l1,l2,x,y,deltaD1,deltaD2):
	m1=2*x*x+(y-l1)*(y-l1)+y*y
	n1=(2-l1)*x*x+(1-l1)*(y-l1)*(y-l1)+y*y
	m2=2*x*x+(y+l2)*(y+l2)+y*y
	n2=(2+l2)*x*x+(1+l2)*(y+l2)*(y+l2)+y*y
	Vy=(deltaD2-deltaD1*m2/m1)/(n2-n1*m2/m1)
	Vx=(deltaD2-deltaD1*n2/n1)/(m2-m1*n2/n1)
	return Vx

def _getVy(l1,l2,x,y,deltaD1,deltaD2):
    	m1=2*x*x+(y-l1)*(y-l1)+y*y
   	n1=(2-l1)*x*x+(1-l1)*(y-l1)*(y-l1)+y*y
    	m2=2*x*x+(y+l2)*(y+l2)+y*y
    	n2=(2+l2)*x*x+(1+l2)*(y+l2)*(y+l2)+y*y

    	Vy=(deltaD2-deltaD1*m2/m1)/(n2-n1*m2/m1)
    	Vx=(deltaD2-deltaD1*n2/n1)/(m2-m1*n2/n1)
    	return Vy
