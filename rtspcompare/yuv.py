
class frame:
    """YUV Frame
    """
    def __init__(self, width, height):
        """Initialize
        """
        ##Number of pixels
        self.pixel = width*height
        ##Y frame
        self.Y = None
        ##U frame
        self.U = None
        ##V frame
        self.V = None

    def parse(self, bytestream):
        """Parse frame from byte stream
        and return remaining byte
        """
        if (len(bytestream) < ((self.pixel/4)*6)):
            raise RuntimeError("Insufficient bytes in stream:"+
                               str((self.pixel/4)*6)+" bytes needed when "+
                               str(len(bytestream))+" is available")
        self.Y = bytestream[:self.pixel]
        self.U = bytestream[self.pixel:(self.pixel/4)*5]
        self.U = bytestream[(self.pixel/4)*5:(self.pixel/4)*6]
        return bytestream[(self.pixel/4)*6:]

class stream:
    """Stream of YUV frames
    """
    def __init__(self, filename, width, height):
        """Initialize
        """
        ##Width of video
        self.width = width
        ##Height of video
        self.height = height
        ##Content
        self.content = []
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
            f = frame(self.width, self.height)
            content = f.parse(content)
            self.content.append(f)

        
