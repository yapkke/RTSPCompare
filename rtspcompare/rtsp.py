import dpkt
import pcap
import struct

class EthernetRTP(dpkt.ethernet.Ethernet):
    """RTP type

    author ykk
    date January 2011
    """
    def __init__(self, pkt, ts):
        """Initialize
        """
        ##Ethernet packet up to UDP
        dpkt.ethernet.Ethernet.__init__(self,pkt)
        ##RTP packet
        try:
            setattr(self["data"]["data"],
                    'data',
                    dpkt.rtp.RTP(self["data"]["data"]["data"]))
        except AttributeError:
            raise KeyError
        ##RTP type expanded
        self.type = self.__get_rtp_type()
        ##Timestamp
        self.ts = ts

    def pkt_size(self):
        """Get packet size
        """
        return len(self.data)

    def get_rtp(self):
        """Get RTP part of packet
        """
        return self["data"]["data"]["data"]

    def __get_rtp_type(self):
        """Parse RTP type
        """
        result = {}
        rtptype = struct.pack("!H",self.get_rtp()["_type"])
        bytes = struct.unpack('!BB',rtptype)

        result["version"] = (bytes[0] & int('11000000',2)) >> 6
        result["padded"] = (((bytes[0] & int('00100000',2)) >> 5) == 1)
        result["extension"] = (((bytes[0] & int('00010000',2)) >> 4) == 1)
        result["csrc_count"] = (bytes[0] & int('00001111',2))        
        result["marked"] = (((bytes[1] & int('10000000',2)) >> 7) == 1)
        result["ptype"] = bytes[1] & int('01111111',2)
        return result

    def __eq__(self, other):
        """Compare packet
        """
        return (self.data == other.data)

class RTPStream:
    """RTP stream

    author ykk
    date January 2011
    """
    def __init__(self, filename, removedup=False):
        """Initialize
        """
        ##List of packets
        self.packets = []
        self.load_file(filename, removedup)
        
    def load_file(self, filename, removedup=False):
        """Load PCAP file
        """
        pc = pcap.pcap(filename)
        pc.setfilter('udp')
        for ts, pkt in pc:
            if (removedup):
                rtppkt = EthernetRTP(pkt,ts)
                if (rtppkt not in self.packets):
                    self.packets.append(rtppkt)
            else:
                self.packets.append(EthernetRTP(pkt,ts))
            
    def ssrc_count(self):
        """Count occurence of each ssrc
        """
        count = {}
        for pkt in self.packets:
            try:
                count[pkt.get_rtp()["ssrc"]] += 1
            except KeyError:
                count[pkt.get_rtp()["ssrc"]] = 1
        return count

    def find_main_ssrc(self):
        """Find the most common ssrc
        """
        count = self.ssrc_count()
        totalcount = 0
        maxkey = None
        maxcount = 0
        for key,c in count.items():
            totalcount += c
            if (c > maxcount):
                maxkey = key
                maxcount = c
        if ((float(maxcount)/float(totalcount)) > 0.9):
            return maxkey
        else:
            return count

    def clean(self, ssrc=None):
        """Clean up non-stream packets and
        reserved payload type 72 or 73
        """
        mssrc = ssrc
        if (ssrc==None):
            mssrc = self.find_main_ssrc()
        if not isinstance(mssrc,dict):
            for pkt in self.packets[:]:
                if ((pkt.get_rtp()["ssrc"] != mssrc) or
                    (pkt.type["ptype"] == 72) or
                    (pkt.type["ptype"] == 73)):
                    self.packets.remove(pkt)
        else:
            raise RuntimeError("File contains multiple stream\n"+str(mssrc))
        
    def __len__(self):
        """Length of stream
        """
        return len(self.packets)

    def marked_count(self):
        """Count number of marked packet
        """
        c = 0
        for pkt in self.packets:
            if pkt.type["marked"]:
                c += 1
        return c

    def padded_count(self):
        """Count number of padded packet
        """
        c = 0
        for pkt in self.packets:
            if pkt.type["padded"]:
                c += 1
        return c

    def capture_ts_list(self):
        """Return list of timestamp of capture
        """
        tsl = []
        for pkt in self.packets:
            tsl.append(pkt.ts)
        return tsl

    def interarrival_ts_list(self):
        """List of interarrival time
        """
        itsl = []
        tsl = self.capture_ts_list()
        for i in range(0, len(tsl)-1):
            itsl.append(tsl[i+1]-tsl[i])
        return itsl

    def pkt_size_list(self):
        """Return list of packet size
        """
        psl = []
        for pkt in self.packets:
            psl.append(pkt.pkt_size())
        return psl

    def seq_list(self):
        """Return list of sequence number
        """
        seql = []
        for pkt in self.packets:
            seql.append(pkt.get_rtp()["seq"])
        return seql

    def timestamp_list(self):
        """Return list of unique timestamps
        """
        tsl = []
        for pkt in self.packets:
            ts = pkt.get_rtp()["ts"]
            if (ts not in tsl):
                tsl.append(ts)
        return tsl

    def frame_no(self):
        """Return number of frames (based on unique timestamps
        """
        return len(self.timestamp_list())
