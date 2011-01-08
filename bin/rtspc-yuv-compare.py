#!/usr/bin/env python

import sys
import getopt
import rtspcompare.yuv as yuv
import struct

def usage():
    """Display usage
    """
    print "Usage "+sys.argv[0]+" <width> <height> <yuv file> <yuv file>\n"+\
          "\n"+\
          "Options:\n"+\
          "-h/--help\n\tPrint this usage guide\n"+\
          ""

#Parse options and arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "hr",
                               ["help"])
except getopt.GetoptError:
    usage()
    sys.exit(2)

#Get options
for opt,arg in opts:
    if (opt in ("-h","--help")):
        usage()
        sys.exit(0)
    else:
        print "Unknown option :"+str(opt)
        sys.exit(2)

#Check there is only width, height and one input file
if not (len(args) == 4):
    usage()
    sys.exit(2)

width=int(args[0])
height=int(args[1])
filename1 = args[2]
filename2 = args[3]

yuvstream1 = yuv.stream(filename1, width, height)
yuvstream2 = yuv.stream(filename2, width, height)

print "Stream 1"
print "No. of frames:\t"+str(len(yuvstream1.content))
print
print "Stream 2"
print "No. of frames:\t"+str(len(yuvstream2.content))

print yuvstream1.avPSNR(yuvstream2)
