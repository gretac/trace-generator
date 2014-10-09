import os
import random
import re


### READ CONFIG FILE ###
config = read_config()

### READ TRACE ###
info = read_trace()


### DETERMINE LENGTH OF TRACE ###
lake = int(len(info))

### INITIALIZE TOTAL ###

if config[1].split()[0] == '1':
    total = event_class()

if config[1].split()[0] == '0':
    total = event()
    


### FINAL AND INITIAL TIMESTAMPS (in microseconds) ###
final_time = int(info[lake-1].split()[0][2:], 16)*(10**(-3))
initial_time = int(info[20].split()[0][2:], 16)*(10**(-3))

### FINAL TIMESTAMP CORRECTED TO SUBTRACT INITIAL TIME ###
correct_time = (final_time) - (initial_time)

### FINAL STATEMENT ###
print "The event of interest occured", total, "times in the trace, which translates to", total/correct_time, "times per microsecond."

def event():
    total = 0
    print lake
    for c in range(lake-1):
            if c < 20:
                c += 20
            x = info[c].split()
            x.extend([""])
            mat = re.match(config[7].split()[0],x[3])
            if mat:
                total +=1
    return total

def event_class():
    for c in range(lake-1):
        if c < 20:
            c += 20
        x = info[c].split()
        mat = re.match(config[4].split()[0],x[2])
        if mat:
            total +=1
    return total

def read_config():
    con = open(os.path.expanduser("~/Documents/python/model/config.txt"),'r')
    config = con.readlines()
    con.close
    return config

def read_trace():
    f = open(os.path.expanduser("~/Documents/traces/car_traces/car1.trace"),'r')
    info = f.readlines()
    f.close
    return info
