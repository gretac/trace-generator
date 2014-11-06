import random
import os

def periodic():
	### INITIALIZE VARIABLES
	timestamp = 0
	cpu = 0
	#event_type = "THREAD"
	event = config[7].strip()
	pid = config[1].strip()
	pid_counter = 1
	tid = 1
	ppid = 0


        ### PROCESS WRITE
        timestamp+=int(config[13])
        tracefile.write('t:' + str(hex(timestamp)) + ' ' + 'CPU:0' + str(cpu) + ' ' + "PROCESS" + ' ' + ":PROCCREATE_NAME" + ' ' + "ppid:" + str(ppid) + ' ' + "pid:" + str(pid) + " " + "name:" + config[4].strip() + '\n')
        
	for y in range(0,20):

		### CONVERT VALUES TO STRINGS FOR WRITE
		c=str(cpu)
		p=str(pid)
		t=str(tid)
		ppid_s = str(ppid)

		### MAIN TIME INCREMENT
                if config[16].strip() == "n":
                        timestamp += int(config[13])
                else:
                        timestamp += int(config[13]) + random.randint(int(config[19]), int(config[22]))
                time=str(hex(timestamp))
                
		### MAIN THREAD WRITE
		tracefile.write('t:' + time + ' ' + 'CPU:0' + c + ' ' + "THREAD" + '  ' + event + '    ' + "pid:" + p + ' ' +"tid:"+ t + ' ' +  '\n')	  
			
	tracefile.close()
"""
def burst():

	### INITIALIZE VARIABLES
	timestamp = 0x1F4
	cpu = 00
	#event_type = "THREAD"
	event = ":THCREATE"
	pid = 1
	pid_counter = 1
	tid = 1
	tid_counter = 1
	ppid = 0

	for y in range(0,10000000):

		### CONVERT VALUES TO STRINGS FOR WRITE
		time=str(hex(timestamp))
		c=str(cpu)
		p=str(pid)
		t=str(tid)
		ppid_s = str(ppid)
		
		###MAIN TIME INCREMENT
		timestamp+=0x1F4
		time=str(hex(timestamp))

		### MAIN THREAD WRITE
		tracefile.write('t:' + time + ' ' + 'CPU:0' + c + ' ' + "THREAD" + '  ' + event + '    ' + "pid:" + '1' + ' ' +"tid:"+ t + ' ' +  '\n')

		### KEEPS TRACK OF TID
		if tid_counter == 2:
			tid += 1
			tid_counter = 0

		### BURST TERM
		if randint(0,10000) == 69:
			tid -= 10
			for j in range(0,10):
				timestamp += 0xA
				time=str(hex(timestamp))
				c=str(cpu)
				p=str(pid)
				t=str(tid)
				ppid_s = str(ppid)
				tracefile.write('t:' + time + ' ' + 'CPU:0' + c + ' ' + "THREAD" + '  ' + ':THRUNNING' + '    ' + "pid:" + p + ' ' +"tid:"+ t + ' ' +  '\n')
				tid += 1
				if j == 9:
					timestamp -=0x64 
			

		### ALTERNATE :THCREATE & :THREADY
		if tid_counter == 1:
			event = ":THREADY "
		else:
			event = ":THCREATE"
		
	
		

		
		pid_counter += 1
		tid_counter += 1
			   
	
	tracefile.close()

def jitter():
	tracefile = open('tracefile.txt','w')

	trace = { "timestamp" : 0xc21886e2, "cpu" : 00, "type" : "THREAD", "event" : ":THCREATE"}
	timestamp = 0
	cpu = 00
	#event_type = "THREAD"
	event = ":THCREATE"
	pid = 1
	pid_counter = 1
	tid = 1
	tid_counter = 1
	ppid = 0


	for y in range(0,1000):
		time=str(hex(timestamp))
		c=str(cpu)
		p=str(pid)
		t=str(tid)
		ppid_s = str(ppid)

		if pid_counter == 1:
			timestamp+=randint(-40,40)
			time=str(hex(timestamp))
			tracefile.write('t:' + time + ' ' + 'CPU:0' + c + ' ' + "PROCESS" + ' ' + ":PROCCREATE_NAME" + ' ' + "ppid:" + ppid_s + ' ' + "pid:" + p + " " + "name:" + "some/directory/goes/here" + '\n')
			ppid += 1
		

		timestamp+=0x1F4
		time=str(hex(timestamp))
		tracefile.write('t:' + time + ' ' + 'CPU:0' + c + ' ' + "THREAD" + '  ' + event + '    ' + "pid:" + p + ' ' +"tid:"+ t + ' ' +  '\n')
	

		event = ":THCREATE"

		if tid_counter == 1:
			event = ":THREADY "

		if pid_counter == 10:
			pid += 1
			tid = 0
			pid_counter = 0
		
		if tid_counter == 2:
			tid += 1
			tid_counter = 0
		
		pid_counter += 1
		tid_counter += 1
	   

	tracefile.close()
	
def random_burst():
	### INITIALIZE VARIABLES
	timestamp = 0
	cpu = 00
	#event_type = "THREAD"
	event = ":THCREATE"
	pid = 1
	pid_counter = 1
	tid = 1
	tid_counter = 1
	ppid = 0

	for y in range(0,10000):

		### CONVERT VALUES TO STRINGS FOR WRITE
		time=str(hex(timestamp))
		c=str(cpu)
		p=str(pid)
		t=str(tid)
		ppid_s = str(ppid)

		### PROCESS WRITE
		if pid_counter == 1:
			timestamp+=0x1F4
			time=str(hex(timestamp))
			tracefile.write('t:' + time + ' ' + 'CPU:0' + c + ' ' + "PROCESS" + ' ' + ":PROCCREATE_NAME" + ' ' + "ppid:" + ppid_s + ' ' + "pid:" + p + " " + "name:" + "some/directory/goes/here" + '\n')
			ppid += 1

		### D500 ROLL   
		if randint(0,500) == 25:
		
			### MAIN TIME INCREMENT
			timestamp+=0xA
			time=str(hex(timestamp))

			### MAIN THREAD WRITE
			tracefile.write('t:' + time + ' ' + 'CPU:0' + c + ' ' + "THREAD" + '  ' + event + '    ' + "pid:" + p + ' ' +"tid:"+ t + ' ' +  '\n')
		
			### ALTERNATE :THCREATE & :THREADY
			if tid_counter == 1:
				event = ":THREADY "
			else:
				event = ":THCREATE"
			
			### KEEPS TRACK OF PID & RESETS TID
			if pid_counter == 10:
				pid += 1
				tid = 0
				pid_counter = 0
			
			### KEEPS TRACK OF TID
			if tid_counter == 2:
				tid += 1
				tid_counter = 0
			
			pid_counter += 1
			tid_counter += 1
				   
			
	tracefile.close()
"""

        
f = open(os.path.expanduser("~/code/config"),'r')
config = f.readlines()
f.close

### CREATE TXT & WRITE HEADER
tracefile = open('trace','w')
tracefile.write("TRACEPRINTER version 1.02\n"+"TRACEPARSER LIBRARY version 1.02\n"+" -- HEADER FILE INFORMATION --\n"+"       TRACE_FILE_NAME:: /dev/shmem/logfile.kev\n"+"            TRACE_DATE:: Mon Oct 28 17:19:14 2013\n"+"       TRACE_VER_MAJOR:: 1\n"+"       TRACE_VER_MINOR:: 01\n"+"   TRACE_LITTLE_ENDIAN:: TRUE\n"+"        TRACE_ENCODING:: 16 byte events\n"+"       TRACE_BOOT_DATE:: Mon Oct 28 11:46:56 2013\n"+"  TRACE_CYCLES_PER_SEC:: 1000000000\n"+"         TRACE_CPU_NUM:: 1\n"+"         TRACE_SYSNAME:: QNX\n"+"        TRACE_NODENAME:: localhost\n"+"     TRACE_SYS_RELEASE:: 6.5.0\n"+"     TRACE_SYS_VERSION:: 2010/07/09-14:44:03EDT\n"+"     TRACE_SYSPAGE_LEN:: 2144\n"+"         TRACE_MACHINE:: x86pc\n"+"-- KERNEL EVENTS --\n")
        
        
if config[10].strip() == "y":
	call = periodic()

if config[1] == 1:
	call = burst()

if config[1] == 2:
	call = jitter()

if config[1] == 3:
	call = random_burst()
