import sys
sys.path.append("./PSK")
sys.path.append("./doppler")

from PSKmain import  PSK2DMulti as _psk
from dopplerMain import dopplermain as _import

def main():
	wave1 = sys.argv[1]
	wave2 = sys.argv[2]
	l1 = 2.10
	l2 = 11.95
	samplerate = 44100
	additionalratio = 10
	debug = 1
	x,y = _psk(wave1,wave2,l1,l2,samplerate,additionalratio,debug)
	
