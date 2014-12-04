import os
import random

f = open(os.path.expanduser("~/code/repos/trace-generator/config"),'r')
config = f.readlines()
f.close

global proc_count
proc_count = int(config[1].strip())	#reads how many processes there are, and converts it to an integer

def confread(pnames, strint):
        dat_list = []
        for c in range(proc_count):
                if strint == "string":
                        dat_list.append(config[c + pnames].strip())
                elif strint == "integer":
                        dat_list.append(int(config[c + pnames].strip()))                        
        return dat_list

def confread2(ploc):
        dat_list = []
        temp_list = []
        for c in range(proc_count):
                temp_list = []
                for k in range(event_count[c]):
                        temp_list.append(config[c + ploc].split()[k])
                dat_list.append(temp_list)
        return dat_list

proc_names = confread(4, "string") #list of process names
pid = confread(3 + (proc_count+3), "integer") #list of process IDs
        
global event_count #global for use in functions 
event_count = confread(3 + (proc_count*2+5), "integer") #list of how many events belong to each process

event_total = 0   #total number of events
for c in range(proc_count):
        event_total += event_count[c]

event_list = confread2(3 + (proc_count*3+7)) #list containing events for each process
tid = confread2(3 + (proc_count*4+9)) #list of thread IDs
event_behav = confread2(3 + (proc_count*5+11)) #list of event behaviours (periodic, random, etc..)
behav_param = confread2(3 + (proc_count*6+13)) #list of parameters for event behaviours
jitter = confread2(3 + (proc_count*7+15)) #list for whether periodic events contain jitter
min_jitter = confread2(3 + (proc_count*8+17)) #list of minimum jitter values
max_jitter = confread2(3 + (proc_count*9+19)) #list of minimum jitter values
burst = confread2(3 + (proc_count*10+21)) #list for whether events exhibit bursty behaviour

### GENERATES A LIST OF BURST PARAMETERS ###
burst_param = []
burst_param_temp = []
i = 0
for c in range(proc_count):
	burst_param_temp = []
        i = 0
	for k in range(event_count[c]):
                if burst[c][k] == "no":
                        burst_param_temp.append(config[3 + (proc_count*11+23) + c].split()[k+i])
                elif burst[c][k] == "yes":
                        for i in range(6):
                                burst_param_temp.append(config[3 + (proc_count*11+23) + c].split()[k+i])
	burst_param.append(burst_param_temp)

### GENERATES A LIST OF EVENT ATTRIBUTES ###
attrib = []
for k in range(proc_count):
        for c in range(event_count[k]):
                attrib.append([proc_names[k], pid[k], event_list[k][c], tid[k][c], event_behav[k][c], behav_param[k][c], jitter[k][c], min_jitter[k][c], max_jitter[k][c], burst[k][c]])

### ADD BURSTY INFORMATION TO ATTRIBUTE LIST... ###
counter = 0
for k in range(proc_count):
        for c in range(event_count[k]):
                if burst[k][c] == "no":
                       attrib[counter].append(burst_param[k][c])
                elif burst[k][c] == "yes":
                       for x in range(6):
                               attrib[counter].append(burst_param[k][c+x])
                counter += 1

### CREATE TRACE & WRITE HEADER ###
tracefile = open(config[3 + (proc_count*12+28)].split()[0],'w')
tracefile.write("TRACEPRINTER version 1.02\n"+"TRACEPARSER LIBRARY version 1.02\n"+" -- HEADER FILE INFORMATION --\n"+"       TRACE_FILE_NAME:: /dev/shmem/logfile.kev\n"+"            TRACE_DATE:: Mon Oct 28 17:19:14 2013\n"+"       TRACE_VER_MAJOR:: 1\n"+"       TRACE_VER_MINOR:: 01\n"+"   TRACE_LITTLE_ENDIAN:: TRUE\n"+"        TRACE_ENCODING:: 16 byte events\n"+"       TRACE_BOOT_DATE:: Mon Oct 28 11:46:56 2013\n"+"  TRACE_CYCLES_PER_SEC:: 1000000000\n"+"         TRACE_CPU_NUM:: 1\n"+"         TRACE_SYSNAME:: QNX\n"+"        TRACE_NODENAME:: localhost\n"+"     TRACE_SYS_RELEASE:: 6.5.0\n"+"     TRACE_SYS_VERSION:: 2010/07/09-14:44:03EDT\n"+"     TRACE_SYSPAGE_LEN:: 2144\n"+"         TRACE_MACHINE:: x86pc\n"+"-- KERNEL EVENTS --\n")

### PROCESS WRITE ###
for i in range(proc_count):
        tracefile.write('t:' + "0" + ' ' + 'CPU:00' + ' ' + "PROCESS" + ' ' + ":PROCCREATE_NAME" + ' ' + "ppid:" + "0" + str(i) + ' ' + "pid:" + str(i+1) + " " + "name:" + proc_names[i] + '\n')

### :THCREATE EVENTS ###
for c in range(proc_count):
        for k in range(event_count[c]):
              tracefile.write("t:" + "0" + " " + "CPU:00" + " " + "THREAD" + "  " + ":THCREATE" + "      " + "pid:" + str(c+1) + " " + "tid:" + str(k+1) + "\n")
        
### CREATE A COUNTER FOR EACH EVENT ###
counter = [0] * event_total  
NEXT = [0] * event_total

### DETERMINES TIMES FOR RANDOM BURSTS ###
rburst_time = []
status = "bad"
while status == "bad":
        rburst_time = []
        for i in range(event_total):
                rburst_time.append([])
                if attrib[i][9] == "yes" and attrib[i][13] == "random":
                        for k in range(int(attrib[i][14])):
                                rburst_time[i].append(random.randint(0 , int(config[3 + (proc_count*12+25)].split()[0])))
                                if k > 0 and (rburst_time[i][k] - rburst_time[i][k-1]) >= int(attrib[i][12]):

                                        status = "BALLER"
                        rburst_time[i] = sorted(rburst_time[i])
'''
## PRINT ATTRIBUTE LISTS ###                
for i in range(len(attrib)):
        print attrib[i]
'''

### CREATING LIST OF BURST INTERVALS ###
burstint = []
for c in range(event_total):
        if attrib[c][9] == 'yes':
                burstint.append(int(attrib[c][12])/(int(attrib[c][11])))
        else:
                burstint.append(0)

### INITIALIZE COUNTERS ###
burstint_mult = [0] * event_total
pcount = [2] * event_total
pburst_count = [1] * event_total
rburst_count = [0] * event_total

### INITIALIZE NEXT VALUES ###
next_options = []
for c in range(len(attrib)):
        next_options.append([])
        next_options[c].append(attrib[c][5])
        next_options[c].append("xxxxx")
        
        if attrib[c][6] == 'yes':       #for periodic behaviour with jitter
                next_options[c][0] = [int(attrib[c][5]) + random.randint( int(attrib[c][7]), int(attrib[c][8]) ), "periodic"]

                if attrib[c][9] == 'yes':       #for bursty shit

                        if attrib[c][13] == 'periodic':   #for periodic bursts
                                next_options[c][1] = [burstint_mult[c] * burstint[c] + int(attrib[c][14]), "bursty"]
                                
                        elif attrib[c][13] == 'random':     #for random bursts
                                next_options[c][1] = [rburst_time[c][0]  , "bursty"]

        elif attrib[c][5] != 'none':    #for periodic behaviour with no jitter
                next_options[c][0] = [int(attrib[c][5]), "periodic"]
                
                if attrib[c][9] == 'yes':       #for bursty shit

                        if attrib[c][13] == 'periodic':   #for periodic bursts
                                next_options[c][1] = [burstint_mult[c] * burstint[c] + int(attrib[c][14]), "bursty"]
                                
                        elif attrib[c][13] == 'random':     #for random bursts
                                next_options[c][1] = [rburst_time[c][0]  , "bursty"]

        NEXT[c] = min(next_options[c])


### BEGIN PRINTING TO TRACE ###
timestamp = 0
while timestamp < int(config[3 + (proc_count*12+25)].split()[0]):
        for c in range(len(attrib)):               
                if NEXT[c][0] != "none" and counter[c] == NEXT[c][0]:
                        tracefile.write("t:" + str(timestamp) + " " + "CPU:00" + " " + "THREAD" + "  " + str(attrib[c][2]) + "      " + "pid:" + str(attrib[c][1]) + " " + "tid:" + str(attrib[c][3]) + "\n")


                        # set new NEXT values
                        if attrib[c][6] == 'yes' and NEXT[c][1] == 'periodic':       #for periodic behaviour with jitter
                                next_options[c][0] = [pcount[c]  * int(attrib[c][5]) + random.randint( int(attrib[c][7]), int(attrib[c][8]) ), "periodic"]
                                pcount[c] += 1


                        elif attrib[c][5] != 'none' and NEXT[c][1] == 'periodic':    #for periodic behaviour with no jitter
                                next_options[c][0] = [pcount[c] * int(attrib[c][5]), "periodic"]
                                pcount[c] += 1


                        if attrib[c][9] == 'yes' and NEXT[c][1] == 'bursty':       #for bursty shit


                                if attrib[c][13] == 'periodic':   #for periodic bursts with no jitter
                                        burstint_mult[c] += 1
                                        if burstint_mult[c] > int(attrib[c][11])-1:
                                                burstint_mult[c] = 0
                                                pburst_count[c] += 1
                                        next_options[c][1] = [burstint_mult[c] * burstint[c] + int(attrib[c][14]) * pburst_count[c], "bursty"]                


                                elif attrib[c][13] == 'random':   #for random bursts
                                        burstint_mult[c] += 1
                                        if burstint_mult[c] > int(attrib[c][11])-1:
                                                burstint_mult[c] = 0
                                                rburst_count[c] += 1

                                        if rburst_count[c] > int(attrib[c][14]) - 1:
                                                next_options[c][1] = ["done", "bursty"]
                                        else:
                                                next_options[c][1] = [burstint_mult[c] * burstint[c] + rburst_time[c][rburst_count[c]], "bursty"] 
                                                
                if NEXT[c] != 'none':
                        NEXT[c] = min(next_options[c])
                counter[c] += 1
        timestamp += 1
                
tracefile.close()
