#!/usr/bin/env python

import sys
import getopt
import numpy
import rtspcompare.rtsp as rtsp

def usage():
    """Display usage
    """
    print "Usage "+sys.argv[0]+" <pcap dump of stream>\n"+\
          "\n"+\
          "Options:\n"+\
          "-s/--ssrc\n\tSpecify synchronized source\n"+\
          "-r/--remove-dup\n\tRemove duplicate packets in trace\n"+\
          "-h/--help\n\tPrint this usage guide\n"+\
          ""

#Parse options and arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "hrs:",
                               ["help","remove-dup","ssrc="])
except getopt.GetoptError:
    usage()
    sys.exit(2)

#Get options
removedup = False
ssrc = None
for opt,arg in opts:
    if (opt in ("-h","--help")):
        usage()
        sys.exit(0)
    elif (opt in ("-r","--remove-dup")):
        removedup = True
    elif (opt in ("-s","--ssrc")):
        ssrc = int(arg)
    else:
        print "Unknown option :"+str(opt)
        sys.exit(2)

#Check there is only one input file
if not (len(args) == 1):
    usage()
    sys.exit(2)

#Get stream and print statistics
rs = rtsp.RTPStream(args[0], removedup)
rs.clean(ssrc)
print "Synchronization source:\t"+str(rs.find_main_ssrc())
print "No. of packets:\t\t\t"+str(len(rs))
print "No. of padded packets:\t\t"+str(rs.padded_count())
print "No. of marked packets:\t\t"+str(rs.marked_count())+\
      " ("+str(float(rs.marked_count())/len(rs))+")"
print "No. of frames:\t\t\t"+str(rs.frame_no())
seql = rs.seq_list()
print "Sequence numbers:\t\t"+str(min(seql))+" -- "+str(max(seql))
psl = rs.pkt_size_list()
print "Packet size:\t\t\t"+str(numpy.mean(psl))+"\t"\
      "("+str(min(psl))+" -- "+str(max(psl))+")"
print "Number Loss:\t\t\t"+str((max(seql)-min(seql)+1)-len(rs))+\
      " ("+str(float((max(seql)-min(seql)+1)-len(rs))/len(rs))+")"
itsl = rs.interarrival_ts_list()
print "Interarrival time:\t\t"+str(numpy.mean(itsl))+"\t"+\
      "("+str(min(itsl))+" -- "+str(max(itsl))+")"
print "Interrarival time stddev:\t"+str(numpy.std(itsl))
print "Jitter:\t\t\t\t"+str(numpy.var(itsl))
