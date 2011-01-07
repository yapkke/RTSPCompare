#!/usr/bin/env python

import sys
import getopt
import rtspcompare.rtsp as rtsp

def usage():
    """Display usage
    """
    print "Usage "+sys.argv[0]+" <pcap dump of stream>\n"+\
          "\n"+\
          "Options:\n"+\
          "-h/--help\n\tPrint this usage guide\n"+\
          ""

#Parse options and arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "h",
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

#Check there is only one input file
if not (len(args) == 1):
    usage()
    sys.exit(2)

#Get stream and print statistics
rs = rtsp.RTPStream(args[0])
rs.clean()
print "Synchronization source:\t"+str(rs.find_main_ssrc())
print "No. of packets:\t\t"+str(len(rs))
print "No. of padded packets:\t"+str(rs.padded_count())
print "No. of marked packets:\t"+str(rs.marked_count())+\
      " ("+str(float(rs.marked_count())/len(rs))+")"
print "No. of frames:\t\t"+str(rs.frame_no())
seql = rs.seq_list()
print "Sequence numbers:\t"+str(min(seql))+"--"+str(max(seql))
print "Number Loss:\t\t"+str((max(seql)-min(seql)+1)-len(rs))
