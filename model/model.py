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
    info = []
    for c in range(tr_count): 
        f = open(os.path.expanduser(config[path_counter].split()[0]),'r')
        info.append(f.readlines())
        f.close
        path_counter += 1
    return info   #info has an entry for each trace, each entry contains a comma separated list of every line in the trace

def event_counter():
    total = []
    time_array = [] 
    for k in range(tr_count):    #for each trace
        total.append(0)       #adding a zero to the array to start counting
        time_array.append([]) #adding an empty sub-array to keep track of timestamps
        for c in range(lake[k]):     #for each line within each trace
            if c < 20:
                c += 20
            x = info[k][c].split()
            x.extend([""])
            mat = re.match(config[10].split()[0],x[3])
            if mat:
                total[k] +=1     #total number of matches for each trace (in a list)
                time_array[k].append(x[0][2:])   #collection of timestamp occurances for each trace (in a list) 

    rate_array = rate_measure(time_array)

    return total, rate_array

def rate_measure(time_array):
    rate_array = []
    for k in range(tr_count):     #for each trace...
        lower_lim = initial_time[k]   # initializes the lower bound
        upper_lim = initial_time[k] + 0xFFFFFF   #initializes the ipper bound
	c = 0
	t = 0
	rate_array.append([])        #adding an empty sub-array to keep track of time intervals
        while upper_lim < final_time[k]:   #until we hit the final timestamp
	    rate_array[k].append(0)        #adds an empty term so there is something to index
	    while (time_array[k][c] < hex(upper_lim)) and (time_array[k][c] > hex(lower_lim)) and c < 100:   #while the timestamp falls between the bounds... THE C CONDITION MUST BE FIXED.
		rate_array[k][t] += 1	 #counts how many timstamps fall within each interval
		c += 1
	    upper_lim += 0xFFFFFF   #bumps up the interval
	    lower_lim += 0xFFFFFF   #bumps up the interval
	    t += 1

    #print rate_array[0]
    #print rate_array[1]
    #print rate_array[2]
	    
    stuff = fluctuation(rate_array)

    return rate_array    #returns an array that shows how many events occurred within each interval of time   

def fluctuation(rate_array):
    mean = []
    diff = []
    for k in range(tr_count):   #for each trace...
	mean_total = 0
	max_diff = 0
	diff.append([])
	mean.append([])
	for c in range(int(len(rate_array[k]))):
	    mean_total += rate_array[k][c]
	mean[k].append(mean_total/int(len(rate_array[k])))		    
	for c in range(int(len(rate_array[k]))):
	    if abs(rate_array[k][c] - mean[k][0]) > max_diff:
		max_diff = abs(rate_array[k][c] - mean[k][0])
	diff[k].append(max_diff)


    # print mean	#DEBUG
    # print diff	#DEBUG

    return mean
    


### READ CONFIG FILE ###
config = read_config()


### SOME GLOBAL VARIABLES ###
global final_time
global initial_time
global lake
global tr_count

# how many traces?
tr_count = int(config[1].strip()[0])

### READ TRACE ###
info = read_trace()

#lake (length of trace)
lake = []
for c in range(tr_count):
    lake.append(int(len(info[c])))

# final_time, initial_time
final_time = []
initial_time = []
correct_time = []
for c in range(tr_count):
    final_time.append(0)
    initial_time.append(0)
    correct_time.append(0)	 
    final_time[c] = (int(info[c][lake[c]-1].split()[0][2:], 16))
    initial_time[c] = (int(info[c][20].split()[0][2:], 16))
    correct_time[c] = ((final_time[c]) - (initial_time[c]))    #timestamp corrected for the non-zero start time


### DETERMINE WHAT IS OF INTEREST ###
if config[4].split()[0] == '1':
    total, rate_array = event_counter()

if config[4].split()[0] == '0':
    total = event_class()        #does not exist btw...


print total[0] / ((final_time[0] - initial_time[0])*10**(-9))
# print "The event of interest occured", total[c], "times in trace",c+1

#

