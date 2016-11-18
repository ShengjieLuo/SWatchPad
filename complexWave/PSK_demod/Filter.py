from readWave import _readwave
from readWave import showwave
import numpy as np
import csv

def Filter18Khz(xf):
    len1=len(xf);
    for i in range(int(len1 * (17.5 / 44))):
        xf[i] = 0 + 0.00000000e+00j;

    for i in range(int(len1 * (18.5 / 44)),len1):
        xf[i] = 0 + 0.00000000e+00j;
    return xf


def Filter17Khz(xf):
    len1=len(xf);
    for i in range(int(len1 * (16.5 / 44))):
        xf[i] = 0 + 0.00000000e+00j;

    for i in range(int(len1 * (17.5 / 44)), len1):
        xf[i] = 0 + 0.00000000e+00j;
    return xf