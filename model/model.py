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
    time_array = [] 
    loop_counter = int(config[1].strip()[0])
    for k in range(loop_counter):    #for each trace
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
                
    mean = time_data(time_array)   #takes mean array from time_data() 
    return total, mean


def time_data(time_array):
    loop_counter = int(config[1].strip()[0])
    inter_array = []
    for k in range(loop_counter):     #for each trace...
        inter_array.append([])        #adding an empty sub-array to keep track of time intervals
        for c in range(int(len(time_array[k]))):   #for the entire length of each collection of timestamps
            if c > 0:
                inter_array[k].append(int(time_array[k][c], 16) - int(time_array[k][c-1], 16))
    mean = mean_time(inter_array)     #takes mean array from mean_time function
    return mean    #passes mean array back to event()   
   
    
def mean_time(inter_array):
	
	loop_counter = int(config[1].strip()[0])
	subtotal = []     #initializing the subtotal value
	mean = []        #initializing the array that will store the mean for each trace
	for k in range(loop_counter):   #for each of the traces...
		subtotal.append(0)   #adding an empty sub-array to store the subtotal for the next trace
		mean.append([])       #adding an empty sub-array to store the mean value for the next trace
		for c in range(len(inter_array[k])):    #for each element in the sub-arrays
			subtotal[k] += inter_array[k][c]
		mean[k].append(subtotal[k]/(len(inter_array[k])))
	
	return mean      #passes mean back to time_data()
			
	
### STILL BROKEN... ###
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
if config[4].split()[0] == '1':
    total, mean = event()

if config[4].split()[0] == '0':
    total = event_class()

### FINAL AND INITIAL TIMESTAMPS (in nanoseconds) ###
for c in range(tr_count): 
	final_time = (int(info[c][lake[c]-1].split()[0][2:], 16))
	initial_time = (int(info[c][20].split()[0][2:], 16))
	correct_time = (final_time) - (initial_time)    #timestamp corrected for the non-zero start time
	 	
	fit = False
	x = 0
	while fit != True:
		if abs(mean[c][0] - (correct_time/total[c])) < x:
			fit = True
		x += 1

	print "The event of interest occured", total[c], "times in trace",c+1, "which deviates from a perfectly periodic function (of period", correct_time/total[c], "nanoseconds), by", x, "nanoseconds on average."
	print ""  

	
	
