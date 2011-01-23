#!/usr/bin/env python

import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
from rtspcompare.psnr import *

for f in sys.argv[1:]:
    (y,u,v) = get_psnr_list(f)
    plt.plot(y)

plt.show()
