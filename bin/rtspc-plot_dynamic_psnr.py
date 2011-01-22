#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy
import sys
from rtspcompare.psnr import *
from rtspcompare.plot import *

def get_ap_combin():
    combination = {}

    combination["unicast"] = ["c","ce","e", "ef" , "f"]
    combination["bicast"] = ["ce","ce","cef","ef","ef"]

    return combination

yvalues = []
xvalues = []
markvalues = []

video = sys.argv[1]
combin = get_ap_combin()
for tx in ["unicast", "bicast"]:
    xv = []
    yv = []
    for pos in range(1,6):
	name = video+"_recv_"+tx+"_"+combin[tx][pos-1]+"_"+str(pos).strip()
        (y, u, v) = get_file_av(name, get_psnr_av)
        xv.append(pos)
        yv.append(yuv_fn(y,u,v))
    yvalues.append(yv)
    xvalues.append(xv)
    if (tx == "unicast"):
        markvalues.append("x--")
    else:
        markvalues.append("o-")
            

for i in range(0, len(yvalues)):
    print str((xvalues[i],yvalues[i]))
    plt.plot(xvalues[i],yvalues[i], markvalues[i])
finalize_plot(plt)
plt.show()


