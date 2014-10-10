import os
import random
import re

def read_config():
    con = open(os.path.expanduser("~/Documents/python/model/config.txt"),'r')
    config = con.readlines()
    con.close
    return config

def read_trace():
    path_counter = 13
    loop_counter = int(config[1].strip()[0])
    info = []
    for c in range(loop_counter):
        #print os.path.expanduser(config[path_counter].split()[0])   #DEBUG
        f = open(os.path.expanduser(config[path_counter].split()[0]),'r')
        info.append(f.readlines())
        f.close
        #print int(len(info))   #DEBUG
        path_counter += 1
    return info

def event():
    total = []
    loop_counter = int(config[1].strip()[0])
    for k in range(loop_counter):
        total.append(0)      #adding a zero to the array to start counting
        for c in range(lake[k]):
            if c < 20:
                c += 20
            x = info[k][c].split()
            x.extend([""])
            mat = re.match(config[10].split()[0],x[3])
            if mat:
                total[k] +=1
    return total

def event_class():
    for c in range(lake-1):
        if c < 20:
            c += 20
        x = info[c].split()
        mat = re.match(config[7].split()[0],x[2])
        if mat:
            total +=1
    return total

### READ CONFIG FILE ###
config = read_config()

### READ TRACE ###
info = read_trace()

### HOW MANY TRACES...?? ###
tr_count = int(config[1].strip()[0])

### DETERMINE LENGTH OF TRACE ###
lake = []
for c in range(tr_count):
    lake.append(int(len(info[c])))

### DETERMINE WHAT IS OF INTEREST ###
if config[4].split()[0] == '0':
    total = event()

if config[4].split()[0] == '1':
    total = event_class()

### FINAL AND INITIAL TIMESTAMPS (in microseconds) ###
for c in range(tr_count): 
    final_time = (int(info[c][lake[c]-1].split()[0][2:], 16)*(10**(-6)))
    initial_time = (int(info[c][20].split()[0][2:], 16)*(10**(-6)))
    correct_time = (final_time) - (initial_time)    #timestamp corrected for the non-zero start time

### FINAL STATEMENT ###
    print "The event of interest occured", total[c], "times in trace",c+1, "which translates to one event occuring every", correct_time/total[c], "milliseconds."


