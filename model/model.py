import os
import random

### READ TRACE ###
f = open(os.path.expanduser("~/Documents/traces/car_traces/car1.trace"),'r')
info = f.readlines()
f.close

print info[20]
