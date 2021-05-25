import os
import sys
from multiprocessing import Queue,Value,Pool
from multiprocessing import Process
import threading
from sys import argv
import re
import time
import signal
import pickle
import datetime
import collections

##################### VARIABLES ############################

global qFiles
qFiles = Queue() # Queue qFiles with files indicated on command line (used when n_processes <= len(files))

global duration
duration = time.time() # initial time

global lines_program
lines_program = Queue()  # Queue lines_program with the lines that have the text of the individual files (used when n_processes > len(files))

current_time = datetime.datetime.now()  # datetime of today

ProcessPool = []  # list with the processes

global Lista_pids
lista_pids = Queue()  # Queue with the pid of the processes (used when n_processes > len(files))

##################### VALUES VARIABLES ############################

# variable value that is the total of lines in all files
total = Value("i", 0)

# Variable value with the count of the text in a line
total_word = Value("i", 0)                 

# Variable value with the sum of all the total_word value
total_words = Value("i", 0)

# variable value with the total number of processed files
processed = Value("i", 0)

# Variable value with the counter to stop the program when ctrl^c is triggered
counter = Value("i", 0)

# Variable value that is the total of words in individual files (used when n_processes > len(files))
total_words_on_individual_file = Value("i",0)

# Variable value that is the total of lines in individual files (used when n_processes > len(files))
total_lines = Value("i", 0)

# Variable value with the final time of the program (used when n_processes > len(files))
final_time = Value("d", 0.0)

##################### LOCK VARIABLES #############################
threadLock = threading.Lock()
mutex = threading.Lock()
mutex_two = threading.Lock()


def converter(Time):
    """
    Converts seconds to hours, minutes, seconds and microseconds.
    Requires: Time, as seconds.
    Ensures:
    - the tempo_final as a str with a format 0:0:0:0.0
    """
    Time = Time % (24 * 3600) 
    hour = Time // 3600

    Time %= 3600
    minutes = Time // 60

    Time %= 60
    seconds = Time

    Time *= 1000
    micro = Time

    tempo_final = "{}:{}:{}:{}".format(int(hour), int(minutes), int(seconds), micro)

    return tempo_final

###################### PROCESS PER FILE METHOD #####################
def processes_bigger_files(line):
    """
    Counts the number of times text appears in line and the number of lines where text is.
    Requires: line, as a list with the division of lines for each process.
    Ensures:
    - the final_time of the program as float
    - total_lines, total, total_word, total_words, total_words_on_individual_file, total_words_file as int
    """
    lista_pids.put(os.getpid())
    search_time = time.time()
    
    for word in line:
        result = re.sub("[^\w]", " ", word).split()
        if text in result:
            mutex.acquire()
            lines_program.put(word.strip()) # puts word (lines) in a queue, so the second process outputs those lines (The queue is needed because they dont share memory)
            total_lines.value += 1 
            total.value += 1 
            total_word.value = result.count(text) 
            total_words.value += total_word.value 
            total_words_on_individual_file.value += total_word.value
            mutex.release()
##                time.sleep(0.1)

    # final time for file processing
    search_time = search_time - duration
    final_time.value = search_time
   
def processes_bigger_files_print(file):
    """
    Recieves the file name, executes the output with all the data from processes_bigger_files function \
    and put that data on a bin file.
    Requires: file, as a str with the name of the file in execution.
    Ensures:
    - Lista_pids, as a queue with the os.getpid()
    - lines_program, as a queue with the lines of the file that have the text
    """
    
    final_time.value = final_time.value % (24 * 3600) 
    hour = final_time.value // 3600

    final_time.value %= 3600
    minutes = final_time.value // 60

    final_time.value %= 60
    seconds = final_time.value

    final_time.value *= 1000
    micro = final_time.value

    tempo_final = "{}:{}:{}:{}".format(int(hour), int(minutes), int(seconds), micro)

    if "-f" in sys.argv:
        while lista_pids.empty() is False:
            with open(log_file, 'ab') as handle:
                if "-c" in sys.argv:
                    mode = "-c"
                    # writes in the log file
                    pickle.dump([lista_pids.get(),file,tempo_final,os.path.getsize(file), total_words_on_individual_file.value, mode], handle, protocol=pickle.HIGHEST_PROTOCOL)
                elif "-l" in sys.argv:
                    mode = "-l"
                    # writes in the log file
                    pickle.dump([lista_pids.get(),file,tempo_final,os.path.getsize(file),total_lines.value, mode], handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    print("\n---------",file,"---------\n")
    while lines_program.empty() is False:
        print(lines_program.get()+"\n")
        
        
    print("\nocorrências de "+"'"+text+"'"+" no ficheiro "+file+" : "+str(total_words_on_individual_file.value))

    mutex_two.acquire()
    processed.value+=1
    total_words_on_individual_file.value = 0
    total_lines.value = 0
    mutex_two.release()

def processes_less_equal_files(qqueue):
    """
    Counts the number of times text appears in line, the number of lines where text is, writes the data \
    inside a bin file and outputs that same data.
    Requires: qqueue, as a queue with the files names.
    Ensures:
    - the search_time of the program as float
    - total_lines, total, total_word, total_words, total_words_on_individual_file, total_words_file as int
    """
    while qqueue.empty() is False:
        if counter.value > 0:  # stops program if ctrl^c is triggered
            exit(0)  #or return 0, works too

        # initial starting time for file processing
        search_time = time.time()

        threadLock.acquire()    
        file = qqueue.get()
        threadLock.release()
        
        source_file = open(file, "r")
        total_words_on_individual_file_int = 0
        total_lines_int = 0
        lines = []
                 
        for line in source_file:
            # replaces inside the line characters there arent alphanumeric with spaces. [^\w] - not alphanumeric
            result = re.sub("[^\w]", " ", line).split()         
            if text in result:
                mutex.acquire()
                lines.append(line.split())
                total_lines_int += 1
                total.value += 1
                total_word.value = result.count(text)
                total_words.value += total_word.value           
                total_words_on_individual_file_int += total_word.value
                mutex.release()
##                time.sleep(0.1)

        # final time for file processing
        search_time = search_time - duration
        
        if "-f" in sys.argv:
            with open(log_file, 'ab') as handle:
                if "-c" in sys.argv:
                    mode = "-c"
                    pickle.dump([os.getpid(),source_file.name,converter(search_time),os.path.getsize(source_file.name), total_words_on_individual_file_int, mode], handle, protocol=pickle.HIGHEST_PROTOCOL) 
                elif "-l" in sys.argv:
                    mode = "-l"
                    pickle.dump([os.getpid(),source_file.name,converter(search_time),os.path.getsize(source_file.name), total_lines_int, mode], handle, protocol=pickle.HIGHEST_PROTOCOL)

        print("\n---------",source_file.name,"---------\n")
        for words in lines:
            print(" ".join(words)+"\n")
            
        print("\nocorrências de "+"'"+text+"'"+" no ficheiro "+source_file.name+" : "+str(total_words_on_individual_file_int))

        source_file.close()
        mutex_two.acquire()
        processed.value+=1
        mutex_two.release()

########################### SIGNALS ############################

def ctrl (sig, NULL): # function used for signal (ctrl+c)
    """
    Stops the program gracefully.
    """
    counter.value += 1
    if counter.value == 1:
        print("\nExiting the program... waiting for the current tasks to finish.")

def print_state(sig, NULL):  # function triggered by ALARM SIGNAL
    """
    Alarm clock with the output of the program data till a certain point.
    """
    print("\nNúmero de ficheiros processados: "+str(processed.value))
    if "-l" in sys.argv:
        print("\nNúmero corrente de linhas onde a palavra foi encontrada: "+str(total.value))
    elif "-c" in sys.argv:
        print("\nNúmero corrente de ocorrências onde a palavra foi encontrada: "+str(total_words.value))

    #calculates current program execution time
    currentDuration = (time.time() - duration)*1000                     
    print("Tempo de execução corrente: "+str(currentDuration)+" microseconds")

########################### BEGIN MAIN PROCESS ####################

signal.signal(signal.SIGINT, ctrl)

if ("-c" in sys.argv or "-l" in sys.argv):
    if "-p" in sys.argv:
        n_processes = sys.argv[sys.argv.index("-p")+1]
        if not n_processes.isdigit():
            raise ValueError("Number of processes must be an integer.")
        else:
            n_processes = int(n_processes)
        start = 5
    else:
        n_processes = 1
        start = 3

    if "-a" in sys.argv:
        time_interval = sys.argv[sys.argv.index("-a")+1]
        if not time_interval.isdigit():
            raise ValueError("Time interval must be a number.")
        else:
            time_interval = float(time_interval)

        start+=2	       
        signal.signal(signal.SIGALRM, print_state)

    if "-f" in sys.argv:
        log_file = sys.argv[sys.argv.index("-f")+1]
        if not ".bin" in log_file:
            raise ValueError("Must be a bin file!")
        else:
            log_file = sys.argv[sys.argv.index("-f")+1]

        start+=2

    if "-f" in sys.argv:
        with open(log_file, 'ab') as handle:
            # writes in the log file the time in which the program has started
            pickle.dump(current_time, handle)

    text = sys.argv[start]
    files = sys.argv[start+1:]

    if len(files) == 0:
        valid = False
        while not valid:
            # Stdin files and splits each file between spaces
            files = input("Indique o(s) ficheiro(s): ").split(" ")   
            valid = True
            for file in files:
                try:
                    test_file=open(file)
                    test_file.close()
                except:
                    print("File "+str(file)+" is not valid. Please try again")
                    valid = False
                    
        for file in files:
            qFiles.put(file)
        if "-a" in sys.argv:
            # SIGNAL that assigns time interval in which print_state function gets triggered
            signal.setitimer(signal.ITIMER_REAL,time_interval,time_interval)

    elif len(files) != 0:
        for file in files:
            # Puts all files in the Queue
            qFiles.put(file)
        if "-a" in sys.argv:
            # SIGNAL that assigns time interval in which print_state function gets triggered
            signal.setitimer(signal.ITIMER_REAL,time_interval,time_interval)

    if n_processes > len(files):
        for file in files:
            if counter.value == 0:
                with open(file) as f:
                    lines = f.readlines()
                    final_lines_divide = [lines[i:i + len(lines)//n_processes] for i in range(0, len(lines), len(lines)//n_processes)]
                    p = Pool(processes = n_processes)
                    p.map(processes_bigger_files, final_lines_divide)
                    p.close()
                    
                p2 = Process(target=processes_bigger_files_print, args=(file, ))
                p2.start()
                ProcessPool.append(p)
                ProcessPool.append(p2)

    elif n_processes <= len(files):
        for i in range(n_processes):
            #start of the process/processes to read all files
            p = Process(target=processes_less_equal_files, args=(qFiles, ))
            p.start()
            ProcessPool.append(p)

    for each in ProcessPool:  
        each.join()

    # calculates final duration of the whole program
    duration = time.time() - duration

    if "-f" in sys.argv:
        with open(log_file, 'ab') as handle:
            # writes in the log file that same duration as seen above
            pickle.dump(converter(duration), handle)

    if "-l" in sys.argv:
        resume = "\n"+"Total de linhas com a palavra "+"'"+text+"'"+" nos ficheiros "+str(", ".join(sys.argv[start+1:])+" ")+": "+str(total.value)+" linhas"
        print(resume)
    elif "-c" in sys.argv:
        resume = "\n"+"Total de ocorrências de "+"'"+text+"'"+" nos ficheiros "+str(", ".join(sys.argv[start+1:])+" ")+": "+str(total_words.value)+" vezes"
        print(resume)

else:
    print("Error: -c or -l must be included on the command line.")                  


########################### END MAIN PROCESS ###########################

