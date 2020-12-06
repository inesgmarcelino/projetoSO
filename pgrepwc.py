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
qFiles = Queue() 

global qlines
qlines = Queue()

global duration
duration = time.time()

global pool_lines
pool_lines = []

global lines_program
lines_program = Queue()

current_time = datetime.datetime.now()

ProcessPool = []

global files_update
files_update = []

global list_pids
list_pids = Queue()


##################### VALUES VARIABLES ############################


total = Value("i", 0)


total_word = Value("i", 0)                 


total_words = Value("i", 0)

total_words_file = Value("i",0)


processed = Value("i", 0)                  

total_words_on_individual_file = Value("i",0)


##################### LOCK VARIABLES #############################
threadLock = threading.Lock()
mutex = threading.Lock()
mutex_two = threading.Lock()


###################### PROCESS PER FILE METHOD #####################
def processes_bigger_files(line):
    """
    """
    
    list_pids.put(os.getpid())
    
    global search_time
    search_time = time.time()
    x = 0

    for word in line:
        result = re.sub("[^\w]", " ", word).split()
        total_lines = 0
        if text in result:
            x += 1
            mutex.acquire()
            lines_program.put(word.strip())
            pool_lines.append(word.strip())
            total_lines += 1
            total.value += 1
            total_word.value = result.count(text)
            total_words.value += total_word.value
            total_words_on_individual_file.value += total_word.value
            total_words_file.value = total_words_on_individual_file.value
            mutex.release()


    search_time = search_time - duration
    
##    if "-f" in sys.argv:
##        with open(log_file, 'ab') as handle:
##            if "-c" in sys.argv:
##                mode = "-c"
##                # writes in the log file
##                pickle.dump([os.getpid(),f.name,search_time,os.path.getsize(f.name), total_words_on_individual_file.value, mode], handle, protocol=pickle.HIGHEST_PROTOCOL)
##            elif "-l" in sys.argv:
##                mode = "-l"
##                # writes in the log file
##                pickle.dump([os.getpid(),f.name,search_time,os.path.getsize(f.name), total_lines, mode], handle, protocol=pickle.HIGHEST_PROTOCOL)
    

##    if qqueue == qlines:
##        while qqueue.empty() is False:
##            # initial starting time for file processing
##            search_time = time.time()
##
##            threadLock.acquire()    
##            line = qqueue.get()
##            threadLock.release()
##            
##            total_lines = 0
##            source_file = open(files[i], "r")
##            print(source_file)
##
##            for word in line:
##                result = re.sub("[^\w]", " ", word).split()
##                
##                if text in result:
##                    mutex.acquire()
##                    lines_program.put(word.strip())
##                    total_lines += 1
##                    total.value += 1
##                    total_word.value = result.count(text)
##                    total_words.value += total_word.value
##                    total_words_on_individual_file.value += total_word.value
##                    total_words_file.value = total_words_on_individual_file.value
##                    mutex.release()
##                    time.sleep(0.1)
##        
##            # final time for file processing
##            search_time = search_time - duration
##            
##            if "-f" in sys.argv:
##                with open(log_file, 'ab') as handle:
##                    if "-c" in sys.argv:
##                        mode = "-c"
##                        # writes in the log file
##                        pickle.dump([os.getpid(),f.name,search_time,os.path.getsize(f.name), total_words_on_individual_file.value, mode], handle, protocol=pickle.HIGHEST_PROTOCOL)
##                    elif "-l" in sys.argv:
##                        mode = "-l"
##                        # writes in the log file
##                        pickle.dump([os.getpid(),f.name,search_time,os.path.getsize(f.name), total_lines, mode], handle, protocol=pickle.HIGHEST_PROTOCOL)

def processes_bigger_files_print(file):
    """
    """
    while list_pids.empty() is False:
        if "-f" in sys.argv:
            with open(log_file, 'ab') as handle:
                if "-c" in sys.argv:
                    mode = "-c"
                    # writes in the log file
                    pickle.dump([list_pids.get(),file,file,os.path.getsize(file), total_words_on_individual_file.value, mode], handle, protocol=pickle.HIGHEST_PROTOCOL)
                elif "-l" in sys.argv:
                    mode = "-l"
                   
                    pickle.dump([list_pids.get(),file,file,os.path.getsize(file), total_lines, mode], handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    print("\n---------",file,"---------\n")
    while lines_program.empty() is False:
        print(lines_program.get()+"\n")
        
        
    print("\nocorrências de "+"'"+text+"'"+" no ficheiro "+file+" : "+str(total_words_file.value))

    mutex_two.acquire()
    processed.value+=1
    total_words_on_individual_file.value = 0
    mutex_two.release()


def processes_less_equal_files(qqueue):
    """
    """
    while qqueue.empty() is False:
    
        search_time = time.time()

        threadLock.acquire()    
        file = qqueue.get()
        threadLock.release()
        
        source_file = open(file, "r")
        total_words_on_individual_file_int = 0
        total_lines = 0
        lines = []
        files_update.append(file)
                 
        for line in source_file:
         
            result = re.sub("[^\w]", " ", line).split()         
            if text in result:
                mutex.acquire()
                lines.append(line.split())
                pool_lines.append(line.split())
                total_lines += 1
                total.value += 1
                total_word.value = result.count(text)
                total_words.value += total_word.value           
                total_words_on_individual_file_int += total_word.value
                total_words_file.value = total_words_on_individual_file_int
                mutex.release()

 
        search_time = search_time - duration
        
        if "-f" in sys.argv:
            with open(log_file, 'ab') as handle:
                if "-c" in sys.argv:
                    mode = "-c"
                    pickle.dump([os.getpid(),source_file.name,search_time,os.path.getsize(source_file.name), total_words_on_individual_file_int, mode], handle, protocol=pickle.HIGHEST_PROTOCOL) 
                elif "-l" in sys.argv:
                    mode = "-l"
                    pickle.dump([os.getpid(),source_file.name,search_time,os.path.getsize(source_file.name), total_lines, mode], handle, protocol=pickle.HIGHEST_PROTOCOL)

        print("\n---------",source_file.name,"---------\n")
        for words in lines:
            print(" ".join(words)+"\n")
            
        print("\nocorrências de "+"'"+text+"'"+" no ficheiro "+source_file.name+" : "+str(total_words_on_individual_file_int))

        source_file.close()
        mutex_two.acquire()
        processed.value+=1
        mutex_two.release()

########################### SIGNALS ############################
def ctrl (sig, NULL): 
    """
    NAO TERMINA QUANDO OS PROCESSOS TERMINAM O PROCESSAMENTO DOS SEUS PRIMEIROS FICHEIROS
##    """
    print(files_update)
    for file in files_update:
        print("\n---------",str(file),"---------\n")
##        for words in pool_lines:
##            print(" ".join(words)+"\n")
##                        
##        print("\nocorrências de "+"'"+text+"'"+" no ficheiro "+str(file)+" : "+str(total_words_file.value))
##                        
        exit(0)


# function triggered by ALARM SIGNAL
def print_state(sig, NULL): 
    """
    FEITO
    """
    print("\nNúmero de ficheiros processados: "+str(processed.value))
    if "-l" in sys.argv:
        print("\nNúmero corrente de linhas onde a palavra foi encontrada: "+str(total.value))
    elif "-c" in sys.argv:
        print("\nNúmero corrente de ocorrências onde a palavra foi encontrada: "+str(total_words.value))

 
    currentDuration = (time.time() - duration)*1000                     
    print("Tempo de execução corrente: "+str(currentDuration)+" microseconds")


########################### BEGIN MAIN PROCESS ####################

# SIGINT signal that triggers function ctrl
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
    
        signal.setitimer(signal.ITIMER_REAL,time_interval,time_interval)

    if "-f" in sys.argv:
        log_file = sys.argv[sys.argv.index("-f")+1]
        if not ".bin" in log_file:
            raise ValueError("Must be a bin file!")
        else:
            log_file = sys.argv[sys.argv.index("-f")+1]

        start+=2

    if "-f" in sys.argv:
        with open(log_file, 'ab') as handle:
     
            pickle.dump(current_time, handle)

    text = sys.argv[start]
    files = sys.argv[start+1:]

    if len(files) == 0:
        valid = False
        while not valid:
       
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

    elif len(files) != 0:
        for file in files:
    
            qFiles.put(file)

    if n_processes > len(files):

##        for i in range(len(files)):
##            with open(files[i]) as f:
##                lines = f.readlines()
####                print(files[i]+"---->"+str(lines))
##                final_lines_divide = [lines[i:i + n_processes] for i in range(0, len(lines), n_processes)]
##                for line in final_lines_divide:
##                    qlines.put(line)


        for file in files:
            files_update.append(file)
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
        
                
        
##            for i in range(len(lines)):
##                line = lines[i]
##                pool_lines.append(line)

                
##
##        final_lines_divide = [pool_lines[i:i + n_processes] for i in range(0, len(pool_lines), n_processes)]
##        for line in final_lines_divide:
##            qlines.put(line)
##    
##        for i in range(n_processes):
##            #start of the process/processes to read all files
##            p = Process(target=processes_bigger_files, args=(qlines, ))
##            p.start()
##
##
##       

##        for i in range(len(files)):
##            p2 = Process(target=processes_bigger_files_print, args=(files[i], ))
##            p2.start()
##            ProcessPool.append(p)
##            ProcessPool.append(p2)

    elif n_processes <= len(files):
        for i in range(n_processes):
      
            p = Process(target=processes_less_equal_files, args=(qFiles, ))
            p.start()
            ProcessPool.append(p)
    
    for each in ProcessPool:
        each.join()


    duration = time.time() - duration

    if "-f" in sys.argv:
        with open(log_file, 'ab') as handle:
         
            pickle.dump(time.strftime("%H:%M:%S:%ms", time.gmtime(duration)), handle) 

    if "-l" in sys.argv:
        resume = "\n"+"Total de linhas com a palavra "+"'"+text+"'"+" nos ficheiros "+str(", ".join(sys.argv[start+1:])+" ")+": "+str(total.value)+" linhas"
        print(resume)
    elif "-c" in sys.argv:
        resume = "\n"+"Total de ocorrências de "+"'"+text+"'"+" nos ficheiros "+str(", ".join(sys.argv[start+1:])+" ")+": "+str(total_words.value)+" vezes"
        print(resume)

else:
    print("Error: -c or -l must be included on the command line.")                  


########################### END MAIN PROCESS ###########################

