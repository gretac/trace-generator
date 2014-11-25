import copy
import os
import random

f = open(os.path.expanduser("~/code/repos/trace-generator/config"),'r')
config = f.readlines()
f.close

proc_count = int(config[1].strip())	#Reads how many processes there are, and converts it to an integer

### GENERATES A LIST OF PROCESS NAMES ###
proc_names = []
for c in range(proc_count):		
	proc_names.append(config[c+4].strip())

### GENERATES A LIST OF PROCESS IDs ###
pid = []
for c in range(proc_count):		
	pid.append(int(config[3 + (proc_count+3) + c]))
        
### GENERATES A LIST OF HOW MANY EVENTS BELONG TO EACH PROCESS ###
event_count = [] 
for c in range(proc_count):
	event_count.append(int(config[3 + (proc_count*2+5) + c]))

### TOTAL NUMBER OF EVENTS ###
event_total = 0
for c in range(proc_count):
        event_total += event_count[c]

### GENERATES A LIST OF LISTS CONTAINING EVENTS FOR EACH PROCESS ###
event_list = []
event_list_temp = []
for c in range(proc_count):
	event_list_temp = []
	for k in range(event_count[c]):
		event_list_temp.append(config[3 + (proc_count*3+7) + c].split()[k])
	event_list.append(event_list_temp)

### GENERATES A LIST OF THREAD IDs ###
tid = []
tid_temp = []
for c in range(proc_count):
	tid_temp = []
	for k in range(event_count[c]):
		tid_temp.append(config[3 + (proc_count*4+9) + c].split()[k])
	tid.append(tid_temp)
        
### GENERATES A LIST OF EVENT BEHAVIOURS ###
event_behav = []
event_behav_temp = []
for c in range(proc_count):
	event_behav_temp = []
	for k in range(event_count[c]):
		event_behav_temp.append(config[3 + (proc_count*5+11) + c].split()[k])
	event_behav.append(event_behav_temp)

### GENERATES A LIST OF EVENT BEHAVIOUR PARAMETERS ###
behav_param = []
behav_param_temp = []
for c in range(proc_count):
	behav_param_temp = []
	for k in range(event_count[c]):
		behav_param_temp.append(config[3 + (proc_count*6+13) + c].split()[k])
	behav_param.append(behav_param_temp)

### GENERATES A LIST FOR WHETHER EVENTS CONTAIN ANY JITTER ###
jitter = []
jitter_temp = []
for c in range(proc_count):
	jitter_temp = []
	for k in range(event_count[c]):
		jitter_temp.append(config[3 + (proc_count*7+15) + c].split()[k])
	jitter.append(jitter_temp)

### GENERATES A LIST FOR MINIMUM JITTER VALUES ###
min_jitter = []
min_jitter_temp = []
for c in range(proc_count):
	min_jitter_temp = []
	for k in range(event_count[c]):
		min_jitter_temp.append(config[3 + (proc_count*8+17) + c].split()[k])
        min_jitter.append(min_jitter_temp)

### GENERATES A LIST FOR MAXIMUM JITTER VALUES ###
max_jitter = []
max_jitter_temp = []
for c in range(proc_count):
	max_jitter_temp = []
	for k in range(event_count[c]):
		max_jitter_temp.append(config[3 + (proc_count*9+19) + c].split()[k])
        max_jitter.append(max_jitter_temp)

### GENERATES A LIST FOR WHETHER EVENTS EXHIBIT BURSTY BEHAVIOUR ### 
burst = []
burst_temp = []
for c in range(proc_count):
	burst_temp = []
	for k in range(event_count[c]):
		burst_temp.append(config[3 + (proc_count*10+21) + c].split()[k])
	burst.append(burst_temp)
        
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

### ADD BURSTY INFORMATION TO ATTRIBUTE LIST...FFFFFFFFFFFFFFFUUUUUUCK!!!!!! ###
counter = 0
for k in range(proc_count):
        for c in range(event_count[k]):
                if burst[k][c] == "no":
                       attrib[counter].append(burst_param[k][c])
                elif burst[k][c] == "yes":
                       for x in range(6):
                               attrib[counter].append(burst_param[k][c+x])
                counter += 1

'''
## PRINT ATTRIBUTE LISTS ###                
for i in range(len(attrib)):
        print attrib[i]
'''

### MAKE A BACKUP COPY OF THE ATTRIBUTE LIST ###
attrib_backup = copy.deepcopy(attrib)

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
counter = [0] * event_total   # for periodic events
burst_counter = [0] * event_total       # for periodic bursts

### CHANGE PERIODS ACCORDING TO JITTER ###
for i in range(event_total):
        if attrib[i][6] == "yes":
                attrib[i][5] = int(attrib[i][5]) + random.randint(int(attrib[i][7]),int(attrib[i][8]))

### DETERMINES TIMES FOR RANDOM BURSTS ###
random_burst_times = []
for i in range(event_total):
        random_burst_times.append([])
        if attrib[i][9] == "yes" and attrib[i][13] == "random":
                for k in range(int(attrib[i][14])):
                        random_burst_times[i].append(random.randint(0 , int(config[3 + (proc_count*12+25)].split()[0])))

'''                        
print random_burst_times                                                     
'''

### BEGIN PRINTING TO TRACE ###
timestamp = 0
random_burst_count = 0
while timestamp < int(config[3 + (proc_count*12+25)].split()[0]):
        for c in range(event_total):
                ### HANDLES PERIODIC BEHAVIOUR ###
                if attrib[c][4] == "periodic" and counter[c] == int(attrib[c][5]):
                        tracefile.write("t:" + str(timestamp) + " " + "CPU:00" + " " + "THREAD" + "  " + attrib[c][2] + "      " + "pid:" + str(attrib[c][1]) + " " + "tid:" + str(attrib[c][3]) + "\n")
                        ### HANDLES JITTER FOR PERIODIC SHIT ###
                        if attrib[c][6] == 'yes':
                                attrib[c][5] = int(attrib_backup[c][5]) + random.randint(int(attrib[c][7]),int(attrib[c][8]))
                        counter[c] = 0

                ### HANDLES RANDOM EVENTS ###
                elif attrib[c][4] == "random" and random.randint(0,100) == 50:
                        tracefile.write("t:" + str(timestamp) + " " + "CPU:00" + " " + "THREAD" + "  " + attrib[c][2] + "      " + "pid:" + str(attrib[c][1]) + " " + "tid:" + str(attrib[c][3]) + "\n")

                ### HANDLES PERIODIC BURSTS ###
                if attrib[c][9] == "yes" and attrib[c][13] == "periodic" and burst_counter[c] == int(attrib[c][14]):
                        burst_timer = 0
                        burst_period = int(attrib[c][12]) / (int(attrib[c][11]) - 1)
                        sub_counter = burst_period
                        while burst_timer <= int(attrib[c][12]): # enter burst loop
                                if sub_counter == burst_period:
                                        tracefile.write("t:" + str(timestamp+burst_timer) + " " + "CPU:00" + " " + "THREAD" + "  " + attrib[c][2] + "      " + "pid:" + str(attrib[c][1]) + " " + "tid:" + str(attrib[c][3]) + "\n")
                                        sub_counter = 0
                                burst_timer += 1
                                sub_counter += 1                                
                        burst_counter[c] = 0



                counter[c] += 1          
                burst_counter[c] += 1
        timestamp += 1


tracefile.close()

'''                        
                ### HANDLES RANDOM BURSTS ###
                if attrib[c][9] == "yes" and attrib[c][13] == "random" and random_burst_count != int(attrib[c][14]):
                        for j in range(len(random_burst_times[c])):
                                if counter[c] == random_burst_times[c][j]:

                                        burst_timer = 0
                                        burst_period = int(attrib[c][12]) / (int(attrib[c][11]) - 1)
                                        sub_counter = burst_period

                                        while burst_timer <= int(attrib[c][12]): # enter burst loop
                                                if sub_counter == burst_period:
                                                        tracefile.write("t:" + str(timestamp+burst_timer) + " " + "CPU:00" + " " + "THREAD" + "  " + attrib[c][2] + "      " + "pid:" + str(attrib[c][1]) + " " + "tid:" + str(attrib[c][3]) + "\n")
                                                        random_burst_count += 1
                                                        sub_counter = 0
                                                burst_timer += 1
                                                sub_counter += 1                                
                                        burst_counter[c] = 0
'''




