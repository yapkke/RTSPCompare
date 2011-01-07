#!/usr/bin/env python

import sys
import getopt
import numpy
import rtspcompare.rtsp as rtsp

def usage():
    """Display usage
    """
    print "Usage "+sys.argv[0]+" <pcap dump of sent stream> <pcap dump of received stream>\n"+\
          "\n"+\
          "Options:\n"+\
          "-r/--remove-dup\n\tRemove duplicate packets in trace\n"+\
          "-h/--help\n\tPrint this usage guide\n"+\
          ""

#Parse options and arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "hr",
                               ["help","remove-dup"])
except getopt.GetoptError:
    usage()
    sys.exit(2)

#Get options
removedup = False
for opt,arg in opts:
    if (opt in ("-h","--help")):
        usage()
        sys.exit(0)
    elif (opt in ("-r","--remove-dup")):
        removedup = True
    else:
        print "Unknown option :"+str(opt)
        sys.exit(2)

#Check there is only two input file
if not (len(args) == 2):
    usage()
    sys.exit(2)

#Get stream and print statistics
rs1 = rtsp.RTPStream(args[0], removedup)
rs2 = rtsp.RTPStream(args[1], removedup)
rs1.clean()
rs2.clean()

if (rs1.find_main_ssrc() != rs2.find_main_ssrc()):
    raise RuntimeError("Dumps are not from the same synchronized source")

print "Synchronization source:\t"+str(rs1.find_main_ssrc())

print
print "Sent"
print "No. of packets:\t\t\t"+str(len(rs1))
print "No. of padded packets:\t\t"+str(rs1.padded_count())
print "No. of marked packets:\t\t"+str(rs1.marked_count())+\
      " ("+str(float(rs1.marked_count())/len(rs1))+")"
print "No. of frames:\t\t\t"+str(rs1.frame_no())
seql = rs1.seq_list()
print "Sequence numbers:\t\t"+str(min(seql))+" -- "+str(max(seql))
psl = rs1.pkt_size_list()
print "Packet size:\t\t\t"+str(numpy.mean(psl))+"\t"\
      "("+str(min(psl))+" -- "+str(max(psl))+")"
print "Number Loss:\t\t\t"+str((max(seql)-min(seql)+1)-len(rs1))+\
      " ("+str(float((max(seql)-min(seql)+1)-len(rs1))/len(rs1))+")"
itsl1 = rs1.interarrival_ts_list()
print "Interarrival time:\t\t"+str(numpy.mean(itsl1))+"\t"+\
      "("+str(min(itsl1))+" -- "+str(max(itsl1))+")"
print "Interrarival time stddev:\t"+str(numpy.std(itsl1))
print "Jitter:\t\t\t\t"+str(numpy.var(itsl1))

print
print "Received"
print "No. of packets:\t\t\t"+str(len(rs2))
print "No. of padded packets:\t\t"+str(rs2.padded_count())
print "No. of marked packets:\t\t"+str(rs2.marked_count())+\
      " ("+str(float(rs2.marked_count())/len(rs2))+")"
print "No. of frames:\t\t\t"+str(rs2.frame_no())
seql = rs2.seq_list()
print "Sequence numbers:\t\t"+str(min(seql))+" -- "+str(max(seql))
psl = rs2.pkt_size_list()
print "Packet size:\t\t\t"+str(numpy.mean(psl))+"\t"\
      "("+str(min(psl))+" -- "+str(max(psl))+")"
print "Number Loss:\t\t\t"+str((max(seql)-min(seql)+1)-len(rs2))+\
      " ("+str(float((max(seql)-min(seql)+1)-len(rs2))/len(rs2))+")"
itsl2 = rs2.interarrival_ts_list()
print "Interarrival time:\t\t"+str(numpy.mean(itsl2))+"\t"+\
      "("+str(min(itsl2))+" -- "+str(max(itsl2))+")"
print "Interrarival time stddev:\t"+str(numpy.std(itsl2))
print "Jitter:\t\t\t\t"+str(numpy.var(itsl2))

print
print "Comparison"
print "Loss in channel:\t\t"+str(len(rs1)-len(rs2))
print "Marked loss in channel:\t\t"+\
      str(rs1.marked_count()-rs2.marked_count())
print "Frame loss in channel:\t\t"+\
      str(rs1.frame_no()-rs2.frame_no())
print "Diff interarrival stddev:\t"+\
      str(numpy.std(itsl2)-numpy.std(itsl1))
