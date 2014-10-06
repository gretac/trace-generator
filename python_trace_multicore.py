from random import *

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

### CREATE TXT & WRITE HEADER
tracefile = open('trace_multi_core.txt','w')
tracefile.write("TRACEPRINTER version 1.02\n"+"TRACEPARSER LIBRARY version 1.02\n"+" -- HEADER FILE INFORMATION --\n"+"       TRACE_FILE_NAME:: /dev/shmem/logfile.kev\n"+"            TRACE_DATE:: Mon Oct 28 17:19:14 2013\n"+"       TRACE_VER_MAJOR:: 1\n"+"       TRACE_VER_MINOR:: 01\n"+"   TRACE_LITTLE_ENDIAN:: TRUE\n"+"        TRACE_ENCODING:: 16 byte events\n"+"       TRACE_BOOT_DATE:: Mon Oct 28 11:46:56 2013\n"+"  TRACE_CYCLES_PER_SEC:: 1000000000\n"+"         TRACE_CPU_NUM:: 1\n"+"         TRACE_SYSNAME:: QNX\n"+"        TRACE_NODENAME:: localhost\n"+"     TRACE_SYS_RELEASE:: 6.5.0\n"+"     TRACE_SYS_VERSION:: 2010/07/09-14:44:03EDT\n"+"     TRACE_SYSPAGE_LEN:: 2144\n"+"         TRACE_MACHINE:: x86pc\n"+"-- KERNEL EVENTS --\n")
tracefile.write('t:' + '1f4' + ' ' + 'CPU:0' + '00' + ' ' + "PROCESS" + ' ' + ":PROCCREATE_NAME" + ' ' + "ppid:" + '0' + ' ' + "pid:" + '1' + " " + "name:" + "some/directory/goes/here" + '\n')

for y in range(0,32):

           
    ###MAIN TIME INCREMENT
    timestamp+=0x1F4
    time=str(hex(timestamp))

    if y == 0:
        event = ":THCREATE"
    if y == 1:
        event = ":THEREADY"
    if y == 2:
        event = ":THRUNNING"
    if y == 3:
        event = ":INT_ENTR"
    if y == 4:
        event = ":INT_HANDLER_ENTR"
    if y == 5:
        event = ":INT_HANDLER_EXIT"
    if y == 6:
        event = ":INT_EXIT"
    if y == 7:
        event = ":THSEND"
    if y == 8:
        event = ":SND_MESSAGE"
    if y == 9:
        event = ":THRECEIVE"
        cpu += 1
    if y == 10:
        event = ":REC_MESSAGE"
    if y == 11:
        event = ":THRUNNING"
    if y == 12:
        event = ":THDEAD"
    if y == 13:
        event = ":THDESTROY"
    if y == 14:
        event = ":THCREATE"
        tid += 1
    if y == 15:
        event = ":THEREADY"
    if y == 16:
        event = ":THRUNNING"
    if y == 17:
        event = ":INT_ENTR"
    if y == 18:
        event = ":INT_HANDLER_ENTR"
    if y == 19:
        event = ":INT_HANDLER_EXIT"
    if y == 20:
        event = ":INT_HANDLER_ENTR"
    if y == 21:
        event = ":INT_HANDLER_EXIT"
    if y == 22:
        event = ":INT_EXIT"
    if y == 23:
        event = ":THSEND"
    if y == 24:
        event = ":SND_MESSAGE"
    if y == 25:
        event = ":THRECEIVE"
        cpu += 2
    if y == 26:
        event = ":REC_MESSAGE"
    if y == 27:
        event = ":THREPLY"
    if y == 28:
        event = ":REPLY_MESSAGE"
    if y == 29:
        event = ":THRUNNING"
    if y == 30:
        event = ":THDEAD"
    if y == 31:
        event = ":THDESTROY"
        
    ### CONVERT VALUES TO STRINGS FOR WRITE
    time=str(hex(timestamp))
    c=str(cpu)
    p=str(pid)
    t=str(tid)
    ppid_s = str(ppid)
 
    ### MAIN THREAD WRITE
    tracefile.write('t:' + time + ' ' + 'CPU:0' + c + ' ' + "THREAD" + '  ' + event + '    ' + "pid:" + '1' + ' ' +"tid:"+ t + ' ' +  '\n')

    ### KEEPS TRACK OF TID
    if tid_counter == 2:
        tid += 1
        tid_counter = 0

    
tracefile.close()








