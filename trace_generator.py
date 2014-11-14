import os

f = open(os.path.expanduser("~/code/trace_generator/config"),'r')
config = f.readlines()
f.close

proc_count = int(config[1].strip())	#Reads how many processes there are, and converts it to an integer

### GENERATES AN ARRAY OF PROCESS NAMES ###
proc_names = []
for c in range(proc_count):		
	proc_names.append(config[c+4].strip())

### GENERATES AN ARRAY OF PROCESS IDs ###
pid = []
for c in range(proc_count):		
	pid.append(int(config[3 + (proc_count+3) + c]))
        
### GENERATES AN OF HOW MANY EVENTS BELONG TO EACH PROCESS ###
event_count = [] 
for c in range(proc_count):
	event_count.append(int(config[3 + (proc_count*2+5) + c]))

### TOTAL NUMBER OF EVENTS ###
event_total = 0
for c in range(proc_count):
        event_total += event_count[c]

### GENERATES AN ARRAY OF ARRAYS CONTAINING EVENTS FOR EACH PROCESS ###
event_list = []
event_list_temp = []
for c in range(proc_count):
	event_list_temp = []
	for k in range(event_count[c]):
		event_list_temp.append(config[3 + (proc_count*3+7) + c].split()[k])
	event_list.append(event_list_temp)

### GENERATES AN ARRAY OF THREAD IDs ###
tid = []
tid_temp = []
for c in range(proc_count):
	tid_temp = []
	for k in range(event_count[c]):
		tid_temp.append(config[3 + (proc_count*4+9) + c].split()[k])
	tid.append(tid_temp)
        
### GENERATES AN ARRAY OF EVENT BEHAVIOURS ###
event_behav = []
event_behav_temp = []
for c in range(proc_count):
	event_behav_temp = []
	for k in range(event_count[c]):
		event_behav_temp.append(config[3 + (proc_count*5+11) + c].split()[k])
	event_behav.append(event_behav_temp)

### GENERATES AN ARRAY OF EVENT BEHAVIOUR PARAMETERS ###
behav_param = []
behav_param_temp = []
for c in range(proc_count):
	behav_param_temp = []
	for k in range(event_count[c]):
		behav_param_temp.append(config[3 + (proc_count*6+13) + c].split()[k])
	behav_param.append(behav_param_temp)


### GENERATES AN ARRAY OF EVENT ATTRIBUTES ###
attrib = []
for k in range(proc_count):
        for c in range(event_count[k]):
                attrib.append([proc_names[k], pid[k], event_list[k][c], tid[k][c], event_behav[k][c], behav_param[k][c]])

'''                
### PRINT ATTRIBUTE LISTS ###                
for i in range(len(attrib)):
        print attrib[i]
'''

### CREATE TRACE & WRITE HEADER
tracefile = open('trace.trace','w')
tracefile.write("TRACEPRINTER version 1.02\n"+"TRACEPARSER LIBRARY version 1.02\n"+" -- HEADER FILE INFORMATION --\n"+"       TRACE_FILE_NAME:: /dev/shmem/logfile.kev\n"+"            TRACE_DATE:: Mon Oct 28 17:19:14 2013\n"+"       TRACE_VER_MAJOR:: 1\n"+"       TRACE_VER_MINOR:: 01\n"+"   TRACE_LITTLE_ENDIAN:: TRUE\n"+"        TRACE_ENCODING:: 16 byte events\n"+"       TRACE_BOOT_DATE:: Mon Oct 28 11:46:56 2013\n"+"  TRACE_CYCLES_PER_SEC:: 1000000000\n"+"         TRACE_CPU_NUM:: 1\n"+"         TRACE_SYSNAME:: QNX\n"+"        TRACE_NODENAME:: localhost\n"+"     TRACE_SYS_RELEASE:: 6.5.0\n"+"     TRACE_SYS_VERSION:: 2010/07/09-14:44:03EDT\n"+"     TRACE_SYSPAGE_LEN:: 2144\n"+"         TRACE_MACHINE:: x86pc\n"+"-- KERNEL EVENTS --\n")

### PROCESS WRITE ###
tracefile.write('t:' + "0" + ' ' + 'CPU:00' + ' ' + "PROCESS" + ' ' + ":PROCCREATE_NAME" + ' ' + "ppid:" + "00" + ' ' + "pid:" + "1" + " " + "name:" + attrib[0][0] + '\n')

### CREATE A COUNTER FOR EACH EVENT ###
counter = []
for i in range(event_total):
        counter.append(i)     #counters are spaces out to prevent simultaneous events occurring at once

timestamp = 0
while timestamp < 1000:
        for c in range(event_total):
                if attrib[c][5] != 'none' and counter[c] == int(attrib[c][5]):
                        tracefile.write("t:" + str(timestamp) + " " + "CPU:00" + " " + "THREAD" + "  " + attrib[c][2] + "      " + "pid:" + str(attrib[c][1]) + " " + "tid:" + str(attrib[c][3]) + "\n")
                        counter[c] = 0
                counter[c] += 1
        timestamp += 1

tracefile.close()


