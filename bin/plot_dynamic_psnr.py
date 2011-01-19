#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy
import sys

def get_ap_combin():
    combination = {}

    combination["unicast"] = ["c","ce","e", "ef" , "f"]
    combination["bicast"] = ["ce","ce","cef","ef","ef"]

    return combination

def get_file_av(prefix, function):
    trun = 10
    sumy = 0.0
    sumu = 0.0
    sumv = 0.0
    for i in range(1, trun+1):
        (y,u,v) = function("psnr_report/"+prefix+"-run"+str(i).strip())
        sumy = sumy + y
        sumu = sumu + u
        sumv = sumv + v
    return (sumy/trun, sumu/trun, sumv/trun)

def get_psnr_list(filename):
    fileRef = open(filename, "r")
    y = []
    u = []
    v = []
    firstline = True
    for line in fileRef:
        if (not firstline):
            val = line.split()
            y.append(float(val[0]))
            u.append(float(val[1]))
            v.append(float(val[2]))
        else:
            firstline = False
    fileRef.close()
    return (y,u,v)

def get_psnr_av(filename):
    (y,u,v) = get_psnr_list(filename)
    return (numpy.average(y),numpy.average(u), numpy.average(v))

def get_psnr_max(filename):
    (y,u,v) = get_psnr_list(filename)
    return (numpy.max(y),numpy.max(u), numpy.max(v))

def get_psnr_min(filename):
    (y,u,v) = get_psnr_list(filename)
    return (numpy.min(y),numpy.min(u), numpy.min(v))

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
        yv.append((4*y+u+v)/6)
    yvalues.append(yv)
    xvalues.append(xv)
    if (tx == "unicast"):
        markvalues.append("x--")
    else:
        markvalues.append("o-")
            

for i in range(0, len(yvalues)):
    print str((xvalues[i],yvalues[i]))
    plt.plot(xvalues[i],yvalues[i], markvalues[i])
#lt.ylim()
#plt.xlim(0.5,5.5)
plt.show()


