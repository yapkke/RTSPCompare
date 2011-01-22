#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy
import sys
from rtspcompare.psnr import *
from rtspcompare.plot import *

def get_ap_combin():
    combination = {}

    combination["unicast"] = ["c","e","f"]
    combination["bicast"] = ["ce","ef"]

    return combination

def get_poss_pos():
    combination = {}
    combination["unicast"] = {}
    combination["bicast"] = {}

    combination["unicast"]["c"] = [1,2]
    combination["unicast"]["e"] = [2,3,4]
    combination["unicast"]["f"] = [4,5]
    
    combination["bicast"]["ce"] = [1,2,3]
    combination["bicast"]["ef"] = [3,4,5]

    return combination

yvalues = []
xvalues = []
markvalues = []

video = sys.argv[1]
combin = get_ap_combin()
poscombin = get_poss_pos()
for tx in ["unicast", "bicast"]:
    for apcombin in combin[tx]:
        xv = []
        yv = []
        for pos in poscombin[tx][apcombin]:
            name = video+"_recv_"+tx+"_"+apcombin+"_"+str(pos).strip()
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


