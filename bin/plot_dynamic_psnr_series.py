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
labels  = []

video = sys.argv[1]
pos = int(sys.argv[2])
run = int(sys.argv[3])

combin = get_ap_combin()
for tx in ["unicast", "bicast"]:
    name = video+"_recv_"+tx+"_"+combin[tx][pos-1]+"_"+str(pos).strip()+"-run"+str(run).strip()
    print name
    (y, u, v) = get_psnr_list("psnr_report/"+name)
    yvalues.append(y)
    xvalues.append(range(0,300))
    labels.append(tx+" ("+update_ap_label(combin[tx][pos-1])+")")
    if (tx == "unicast"):
        markvalues.append("x--")
    else:
        markvalues.append("o-")
            

for i in range(0, len(yvalues)):
    #print str((xvalues[i],yvalues[i]))
    plt.plot(xvalues[i],yvalues[i], markvalues[i])
plt.legend(labels)
#finalize_plot(plt)
plt.show()


