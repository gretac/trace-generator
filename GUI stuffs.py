from Tkinter import *
from random import *

def button1click():
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
    y = 0
   

    ### CREATE TXT & WRITE HEADER
    tracefile = open('GUI_trace.txt','w')
    tracefile.write("TRACEPRINTER version 1.02\n"+"TRACEPARSER LIBRARY version 1.02\n"+" -- HEADER FILE INFORMATION --\n"+"       TRACE_FILE_NAME:: /dev/shmem/logfile.kev\n"+"            TRACE_DATE:: Mon Oct 28 17:19:14 2013\n"+"       TRACE_VER_MAJOR:: 1\n"+"       TRACE_VER_MINOR:: 01\n"+"   TRACE_LITTLE_ENDIAN:: TRUE\n"+"        TRACE_ENCODING:: 16 byte events\n"+"       TRACE_BOOT_DATE:: Mon Oct 28 11:46:56 2013\n"+"  TRACE_CYCLES_PER_SEC:: 1000000000\n"+"         TRACE_CPU_NUM:: 1\n"+"         TRACE_SYSNAME:: QNX\n"+"        TRACE_NODENAME:: localhost\n"+"     TRACE_SYS_RELEASE:: 6.5.0\n"+"     TRACE_SYS_VERSION:: 2010/07/09-14:44:03EDT\n"+"     TRACE_SYSPAGE_LEN:: 2144\n"+"         TRACE_MACHINE:: x86pc\n"+"-- KERNEL EVENTS --\n")

    while y < trace_length_box.get():

        ### CONVERT VALUES TO STRINGS FOR WRITE
        time=str(hex(timestamp))
        c=str(cpu)
        p=str(pid)
        t=str(tid)
        ppid_s = str(ppid)

        ### PROCESS WRITE
        if pid_counter == 1:
            timestamp+=randint(0,40)
            time=str(hex(timestamp))
            tracefile.write('t:' + time + ' ' + 'CPU:0' + c + ' ' + "PROCESS" + ' ' + ":PROCCREATE_NAME" + ' ' + "ppid:" + ppid_s + ' ' + "pid:" + p + " " + "name:" + "some/directory/goes/here" + '\n')
            ppid += 1

        ### MAIN TIME INCREMENT
        timestamp+=0x1F4
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
                          
        y += 1
    tracefile.close()


root = Tk()
root.title('Trace simulator 3000 MK. II a-spec Xtreme+ turbo')

 
contain1 = Frame(root)
contain1.pack()

trace_length_l = Label(contain1)
trace_length_l['text'] = "Enter Trace Time (nanoseconds)"
trace_length_l.pack(side=LEFT)

trace_length_box = Entry(contain1)
trace_length_box.pack(side=LEFT)

button1 = Button(root, text = "Generate trace", command=button1click)        
button1.pack()





root.mainloop()
