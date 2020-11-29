import os
##import sys
from multiprocessing import Queue,Value,Pool
from multiprocessing import Process
import threading
from sys import argv
import re
import time
import signal
import pickle
import datetime



##################### GLOBAL VARIABLES ############################

global qFiles
qFiles = Queue() # Queue qFiles with files indicated on command line

global duration
duration = time.time()

global lines
lines = Queue()

global files_update
files_update = []

ProcessPool = []


##################### VALUES VARIABLES ############################

total = Value("i", 0)                      # variable value that is going to be the position of list qFiles
total_word = Value("i", 0)                 # Variable value with the count of the text in a line
total_words = Value("i", 0)                # Variable value with the sum of all the total_word value
total_words_file = Value("i",0)
processed = Value("i", 1)                  # variable value with the total number of processed files
##counter = Value("i", 0)
position = Value("i", 0)
total_words_on_individual_file = Value("i", 0)


##################### LOCKS VARIABLES #############################
threadLock = threading.Lock()
mutex = threading.Lock()
mutex_two = threading.Lock()


########################### BEGIN MAIN PROCESS ####################

if ("-c" in sys.argv or "-l" in sys.argv):
    if "-p" in sys.argv:
        n_processes = sys.argv[sys.argv.index("-p")+1]
        if not n_processes.isdigit():
            raise("Number of processes must be an integer.")
        else:
            n_processes = int(n_processes)
        start = 5
    else:
        n_processes = 1
        start = 3

    if "-a" in sys.argv:
        time_interval = sys.argv[sys.argv.index("-a")+1]
        if not time_interval.isdigit():
            raise("Time interval must be a number")
        else:
            time_interval = float(time_interval)

        start+=2	       
        signal.signal(signal.SIGALRM, print_state)                     
        signal.setitimer(signal.ITIMER_REAL,time_interval,time_interval) # SIGNAL that assigns time interval in which print_state function gets triggered

    if "-f" in sys.argv:
        log_file = sys.argv[sys.argv.index("-f")+1]
        if not ".bin" in log_file:                       # In case the user forgets to put the name file or the .bin on file
            start+=1
            valid = True
            while not valid:
                log_file = input("Deseja indicar o nome do ficheiro bin (Se 'n' o ficheiro será Default.bin) (y/n): ")
                if log_file == "y":
                    log_file = input("Indique o nome do ficheiro bin (name_file.bin): ")
                    if not ".bin" in log_file:
                        valid = True
                    else:
                        valid = False
                elif log_file == "n":
                    log_file = "Default.bin"
                    valid = False
        elif ".bin" in log_file:
            log_file = sys.argv[sys.argv.index("-f")+1]
            start+=2

    text = sys.argv[start]
    files = sys.argv[start+1:]

    if len(files) == 0:
        valid = False
        while not valid:
            files = input("Indique o(s) ficheiro(s): ").split(" ")   # Stdin files and splits each file between spaces
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

    elif len(files) != 0:
        for i in files:
            qFiles.put(i)                    # Puts all files in the Queue


    current_time=datetime.datetime.now()
    if "-f" in sys.argv:
        with open(log_file, 'ab') as handle:
            pickle.dump(current_time, handle, -1)    # writes in the log file the time in which the program has started

    defining_numberP_to_Files_or_lines()

    signal.signal(signal.SIGINT, ctrl)      # SIGINT signal that triggers function ctrl  ??

    for each in ProcessPool:
        each.join()
    
    duration = time.time() - duration  # calculates final duration of the whole program

    if "-f" in sys.argv:
        with open(log_file, 'ab') as handle:
            pickle.dump(time.strftime("%H:%M:%S:%ms", time.gmtime(duration)), handle, -1) # writes in the log file that same duration as seen above

    total()

else:
    print("Error: -c or -l must be included on the command line.")                  


########################### END MAIN PROCESS ###########################


########################### DEFINING METHODS TO USE ####################
def defining_numberP_to_Files_or_lines():

    if n_processes > len(files):
        for file in files:
            with open(file) as source_file:
                original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
                p = Pool(processes = n_processes)
                signal.signal(signal.SIGINT, original_sigint_handler)
                p.map(processes_bigger_files, source_file)
                p.close()

            p_main = Process(target=processes_bigger_files_print, args=(i, ))
            p_main.start()
            ProcessPool.append(p)
            ProcessPool.append(p_main)

    elif n_processes <= len(files):
        for i in range(n_processes):
            p = Process(target=processes_less_equal_files, args=(i, ))
            p.start()
            ProcessPool.append(p)

###################### PROCESS PER LINE METHOD ######################
def processes_bigger_files(line):
    """
    FEITO
    """
    
    files_update.append(source_file.name)
    search_time = time.time()                               # initial starting time for file processing
    result = re.sub("[^\w]", " ", line).split()         # replaces inside the line characters there arent alphanumeric with spaces. [^\w] - not alphanumeric
    total_lines = 0

    if text in result:
        mutex.acquire()
        lines.put(line.strip())
        total_lines += 1
        total.value += 1
        total_word.value = result.count(text)
        total_words.value += total_word.value           
        total_words_on_individual_file.value += total_word.value
        total_words_file.value = total_words_on_individual_file.value
        mutex.release()

    search_time = duration - search_time
    time.sleep(0.2)

    if "-f" in sys.argv:
        with open(log_file, 'ab') as handle:
            if "-c" in sys.argv:
                mode = "-c"
                pickle.dump([os.getpid(),read_file.name,search_time,os.path.getsize(read_file.name), total_words_on_individual_file.value, mode], handle, protocol=pickle.HIGHEST_PROTOCOL) # writes in the log file
            elif "-l" in sys.argv:
                mode = "-l"
                pickle.dump([os.getpid(),read_file.name,search_time,os.path.getsize(read_file.name), total_lines, mode], handle, protocol=pickle.HIGHEST_PROTOCOL)  

###################### PROCESS PER FILE METHOD #####################
def processes_less_equal_files(line):               
    """
    Processes read files

    Requires:
    - ind, an int of the specific process;
    Ensures:
    - prints lines where the word is indicated \
      and the number of ocurrences of the word in individual files.
    """

    while qFiles.empty() is False:
        threadLock.acquire()
        file = qFiles.get()
        threadLock.release()
        read_file = open(file, "r")
        files_update.append(read_file)
        total_words_on_individual_file = 0
        total_lines = 0
        search_time = time.time()                               # initial starting time for file processing

        for line in read_file:
            result = re.sub("[^\w]", " ", line).split()         # replaces inside the line characters there arent alphanumeric with spaces. [^\w] - not alphanumeric
            if text in result:
                mutex.acquire()
                lines.put(line.strip())
                total_lines += 1
                total.value += 1
                total_word.value = result.count(text)
                total_words.value += total_word.value           
                total_words_on_individual_file += total_word.value
                total_words_file.value = total_words_on_individual_file
                time.sleep(0.3)
                mutex.release()
                
        search_time = duration - search_time

        if "-f" in sys.argv:
            with open(log_file, 'ab') as handle:
                if "-c" in sys.argv:
                    mode = "-c"
                    pickle.dump([os.getpid(),read_file.name,search_time,os.path.getsize(read_file.name), total_words_on_individual_file, mode], handle, protocol=pickle.HIGHEST_PROTOCOL) # writes in the log file
                elif "-l" in sys.argv:
                    mode = "-l"
                    pickle.dump([os.getpid(),read_file.name,search_time,os.path.getsize(read_file.name), total_lines, mode], handle, protocol=pickle.HIGHEST_PROTOCOL) # writes in the log file

        processes_bigger_files_print(read_file.name)

        read_file.close()

###################### OUTPUT PER FILE ########################
def processes_bigger_files_print(source_file):
    """
    """
    print("\n---------",source_file,"---------\n")
    while lines.empty() is False:
        print(lines.get()+"\n")
        
    print("\nocorrências de "+"'"+text+"'"+" no ficheiro "+source_file+" : "+str(total_words_file.value))

    mutex_two.acquire()
    processed.value+=1
    total_words_on_individual_file.value = 0
##    counter.value+=1
    mutex_two.release()

###################### TOTAL OUTPUT ###########################
def total():
    if "-l" in sys.argv:
        resume = "\n"+"Total de linhas com a palavra "+"'"+text+"'"+" nos ficheiros "+str(", ".join(files)+" ")+": "+str(total.value)+" linhas"
        print(resume)
    elif "-c" in sys.argv:
        resume = "\n"+"Total de ocorrências de "+"'"+text+"'"+" nos ficheiros "+str(", ".join(files)+" ")+": "+str(total_words.value)+" vezes"
        print(resume)

########################### SIGNALS ############################
def ctrl (sig, NULL): 
    """
    NAO TERMINA QUANDO OS PROCESSOS TERMINAM O PROCESSAMENTO DOS SEUS PRIMEIROS FICHEIROS
##    """
    for i in range(len(files_update)):
        print("\n---------",str(files_update[i].name),"---------\n")
        for words in lines:
            print(" ".join(words)+"\n")
                        
        print("\nocorrências de "+"'"+text+"'"+" no ficheiro "+str(files_update[i].name)+" : "+str(total_words_file.value))
        sys.exit()

def print_state(sig, NULL): # function triggered by ALARM SIGNAL
    """
    FEITO
    """
    print("\nNúmero de ficheiros processados: "+str(processed.value))
    if "-l" in sys.argv:
        print("\nNúmero corrente de linhas onde a palavra foi encontrada: "+str(total.value))
    elif "-c" in sys.argv:
        print("\nNúmero corrente de ocorrências onde a palavra foi encontrada: "+str(total_words.value))
    currentDuration = (time.time() - duration)*1000 #calculates current program execution time
    print("Tempo de execução corrente: "+str(currentDuration)+" microseconds")
