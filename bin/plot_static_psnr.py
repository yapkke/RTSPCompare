#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy
import sys

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

def get_psnr_q1(filename):
    (y,u,v) = get_psnr_list(filename)
    y.sort()
    u.sort()
    v.sort()
    index = int(len(y)/4)
    return (y[index],u[index], v[index])

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
poscombin = get_poss_pos()
for tx in ["unicast", "bicast"]:
    for apcombin in combin[tx]:
        xv = []
        yv = []
        for pos in poscombin[tx][apcombin]:
            name = video+"_recv_"+tx+"_"+apcombin+"_"+str(pos).strip()
            (y, u, v) = get_file_av(name, get_psnr_q1)
            xv.append(pos)
            yv.append(y)
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


