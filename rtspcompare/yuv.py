import struct
import math
import commands

class bareframe:
    """Bare YUV frame without breaking YUV value
    """
    def __init__(self, width, height):
        ##Number of pixels
        self.pixel = width*height
        ##Binary string
        self.__string = None

    def parse(self, bytestream):
        """Parse frame from byte stream
        and return remaining byte
        """
        if (len(bytestream) < ((self.pixel/4)*6)):
            raise RuntimeError("Insufficient bytes in stream:"+
                               str((self.pixel/4)*6)+" bytes needed when "+
                               str(len(bytestream))+" is available")
        self.__string = bytestream[:(self.pixel/4)*6]
        return bytestream[(self.pixel/4)*6:]

    def __str__(self):
        """Return binary string
        """
        return self.__string

class frame(bareframe):
    """YUV Frame
    """
    def __init__(self, width, height):
        """Initialize
        """
        bareframe.__init__(self, width, height)
        ##Y frame
        self.Y = None
        ##U frame
        self.U = None
        ##V frame
        self.V = None

    def unpack(self, string):
        """Unpack binary string
        """
        return struct.unpack('B'*len(string), string)

    def parse(self, bytestream):
        """Parse frame from byte stream
        and return remaining byte
        """
        if (len(bytestream) < ((self.pixel/4)*6)):
            raise RuntimeError("Insufficient bytes in stream:"+
                               str((self.pixel/4)*6)+" bytes needed when "+
                               str(len(bytestream))+" is available")
        self.Y = self.unpack(bytestream[:self.pixel])
        self.U = self.unpack(bytestream[self.pixel:(self.pixel/4)*5])
        self.V = self.unpack(bytestream[(self.pixel/4)*5:(self.pixel/4)*6])
        return bytestream[(self.pixel/4)*6:]

    def __PSNR(self, refFrame, frame):
        """Calculate PSNR of frame against reference frame
        """
        errSquared = 0
        for i in range(0, len(refFrame)):
            errSquared += math.pow(refFrame[i] - frame[i], 2.0)
        return 20*math.log10(255/math.sqrt(errSquared/len(refFrame)))

    def Y_PSNR(self, frame):
        """Calculate PSNR with this Y frame as reference
        """
        return self.__PSNR(self.Y, frame.Y)

    def U_PSNR(self, frame):
        """Calculate PSNR with this U frame as reference
        """
        return self.__PSNR(self.U, frame.U)

    def V_PSNR(self, frame):
        """Calculate PSNR with this V frame as reference
        """
        return self.__PSNR(self.V, frame.V)

    def PSNR(self, frame):
        """Calculate PSNR with output for (Y,U,V)
        """
        return (self.Y_PSNR(frame),
                self.U_PSNR(frame),
                self.V_PSNR(frame))

class barestream:
    """Bare YUV stream, where frame is stored as rare bytes
    """
    def __init__(self, filename, width, height):
        ##Width of video
        self.width = width
        ##Height of video
        self.height = height
        ##Content
        self.content = []
        if (filename != None):
            self.__read_file(filename)

    def __read_file(self, filename):
        """Read YUV file
        """
        fileRef = open(filename, "r")
        content = ""
        for b in fileRef:
            content+=b
        fileRef.close()

        while (len(content) != 0):
            f = bareframe(self.width, self.height)
            content = f.parse(content)
            self.content.append(f)

    def dup_frame(self, i):
        """Duplicate frame of index
        """
        self.content.insert(i,self.content[i])

    def clone(self):
        """Clone stream
        """
        cl = barestream(None, self.width, self.height)
        cl.content = self.content[:]
        return cl

    def __str__(self):
        """Return YUV stream
        """
        string = ""
        for f in self.content:
            string += str(f)
        return string

    def write(self, filename):
        """Write YUV stream to file
        """
        fileRef = open(filename, "w")
        fileRef.write(str(self))
        fileRef.close()

class stream(barestream):
    """Stream of YUV frames
    """
    def __init__(self, filename, width, height):
        """Initialize
        """
        barestream.__init__(self, None, width, height)
        if (filename != None):
            self.__read_file(filename)        

    def clone(self):
        """Clone stream
        """
        cl = stream(None, self.width, self.height)
        cl.content = self.content[:]
        return cl

    def __read_file(self, filename):
        """Read YUV file
        """
        fileRef = open(filename, "r")
        content = ""
        for b in fileRef:
            content+=b
        fileRef.close()

        while (len(content) != 0):
            f = frame(self.width, self.height)
            content = f.parse(content)
            self.content.append(f)
    
    def PSNR(self, stream):
        """Calculate PSNR between stream
        """
        psnr = []
        for i in range(0,len(stream.content)):
            psnr.append(self.content[i].PSNR(stream.content[i]))
            print str(i)+"\t"+str(psnr[-1])
        return psnr

    def avPSNR(self, stream):
        """Calculate PSNR between stream
        """
        psnr = 0.0
        for i in range(0,len(stream.content)):
            psnr += sum(self.content[i].PSNR(stream.content[i]))
        return (psnr/float(len(stream.content)))

    def extend(self, refStream):
        """Extend stream by one to maximize avPSNR with reference
        """
        print "Extending stream"
        avPSNR = 0
        bestFrame = None
        for i in range(0, len(self.content)):
            cl = self.clone()
            cl.dup_frame(i)
            cPSNR = refStream.avPSNR(self)
            if (cPSNR > avPSNR):
                avPSNR = cPSNR
                bestFrame = i
            print "Frame "+str(i)+" yield average PSNR of "+str(cPSNR)
        self.dup_frame(bestFrame)
