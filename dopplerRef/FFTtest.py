import numpy as np
import matplotlib.pyplot as plt
t = np.arange(256)
print t
sp = np.fft.fft(np.sin(t))
print sp
freq = np.fft.fftfreq(t.shape[-1])
plt.plot(freq, sp.real, freq, sp.imag)
plt.show()
