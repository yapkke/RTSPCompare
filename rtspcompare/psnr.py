import numpy

def yuv_fn(y,u,v):
    return (4*y+u+v)/6

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
