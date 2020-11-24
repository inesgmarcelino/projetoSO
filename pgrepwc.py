import os
import sys
from multiprocessing import Queue,Value,Semaphore,Manager,Array
from multiprocessing import Process
import threading
from sys import argv
from sys import stdin
import re
import time
import signal
import pickle
import datetime
from ctypes import c_char_p


##################### VARIAVEIS GLOBAIS ###############################

global qFiles
qFiles = Queue()  # Queue qFiles with files indicated on command line

global duration
duration = time.time()

global l
l = []

total = Value("i", 0)                      # variable value that is going to be the position of list qFiles
total_word = Value("i", 0)                 # Variable value with the count of the text in a line
total_words = Value("i", 0)                # Variable value with the sum of all the total_word value
processed = Value("i", 1)                  # variable value with the total number of processed files
##total_words_individual_files = Array(c_char_p, [])
total_words_individual_files = Value("i", 0)
threadLock = threading.Lock()
mutex = threading.Lock()
mutex_two = threading.Lock()



##################### FINAL VARIAVEIS GLOBAIS ###############################


########################### SIGNALS #######################################
def ctrl (sig, NULL): 
    """
    ESTÁ ERRADO. ERROS NO VALOR DE TOTAL, NAO TERMINA QUANDO OS PROCESSOS TERMINAM O PROCESSAMENTO DOS SEUS PRIMEIROS FICHEIROS
    """
    if "-l" in sys.argv:
        for i in range(len(l)):
            print("\nocorrências de "+"'"+text+"'"+" no ficheiro "+str(l[i])+" : "+str(total_words_individual_files.value)+"\n"+"Total de linhas com a palavra "+"'"+text+"'"+" nos ficheiros processados: "+str(total.value)+" linhas")
            sys.exit()
    if "-c" in sys.argv:
        for i in range(len(l)):
            print("\nocorrências de "+"'"+text+"'"+" no ficheiro "+str(l[i])+" : "+str(total_words_individual_files.value)+"\n"+"Total de ocorrências de "+"'"+text+"'"+" nos ficheiros processados: "+str(total_words.value)+" vezes")
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


########################### FINAL SIGNALS #######################################


########################### METODOS #######################################
def processes_bigger_files(ind):
    """
    FALTA DEFINIR SE PROCESSOS MAIOR QUE FICHEIROS, DIVIDIR OS FICHEIROS, O PROBLEMA ESTA PROVAVELMENTE NO FILE = QfILES.GET()
    """
    threadLock.acquire()
    file = qFiles.get()
    l.append(file)
    threadLock.release()

    read_file = open(file, "r")
    lines = []
    search_time = time.time()                               # initial starting time for file processing
    total_lines = 0
    total_words_on_individual_file = 0

    for line in read_file:
        result = re.sub("[^\w]", " ", line).split()         # replaces inside the line characters there arent alphanumeric with spaces. [^\w] - not alphanumeric
        if text in result:
            mutex.acquire()
            lines.append(line.strip())
            total_lines += 1
            total.value += 1
            total_word.value = result.count(text)
            total_words.value += total_word.value           
            total_words_on_individual_file += total_word.value
            mutex.release()

    search_time = duration - search_time
    time.sleep(2)

    print("\n---------",read_file.name,"---------\n")
    for words in lines:
        print(" ".join(words)+"\n")
        
    print("\nocorrências de "+"'"+text+"'"+" no ficheiro "+read_file.name+" : "+str(total_words_on_individual_file))
    read_file.close()


def processes_less_equal_files(ind):
    """
    FEITO
    """
    threadLock.acquire()
    file = qFiles.get()
    l.append(file)
    threadLock.release()

    read_file = open(file, "r")
    lines = []
    search_time = time.time()                               # initial starting time for file processing
    total_lines = 0
    total_words_on_individual_file = 0

    for line in read_file:
        result = re.sub("[^\w]", " ", line).split()         # replaces inside the line characters there arent alphanumeric with spaces. [^\w] - not alphanumeric
        if text in result:
            mutex.acquire()
            lines.append(line.strip())
            total_lines += 1
            total.value += 1
            total_word.value = result.count(text)
            total_words.value += total_word.value           
            total_words_on_individual_file += total_word.value
            mutex.release()

    search_time = duration - search_time
    time.sleep(2)
    print("\n---------",read_file.name,"---------\n")
    for words in lines:
        print(" ".join(words)+"\n")
        
    print("\nocorrências de "+"'"+text+"'"+" no ficheiro "+read_file.name+" : "+str(total_words_on_individual_file))
    read_file.close()

def read_files(ind):   # metodo main               
    """
    Processes read files

    Requires:
    - ind, an int of the specific process;
    Ensures:
    - prints lines where the word is indicated \
      and the number of ocurrences of the word in individual files.
    """
    
    while qFiles.empty() is False:

        if n_processes > len(files):
            processes_bigger_files(ind)

        else:
            processes_less_equal_files(ind)

        if "-f" in sys.argv:
            with open(log_file, 'ab') as handle:
                if "-c" in sys.argv:
                    mode = "-c"
                    pickle.dump([os.getpid(),read_file.name,search_time,os.path.getsize(read_file.name), total_words_on_individual_file, mode], handle, protocol=pickle.HIGHEST_PROTOCOL) # writes in the log file
                elif "-l" in sys.argv:
                    mode = "-l"
                    pickle.dump([os.getpid(),read_file.name,search_time,os.path.getsize(read_file.name), total_lines, mode], handle, protocol=pickle.HIGHEST_PROTOCOL) # writes in the log file
                    
        mutex_two.acquire()
        processed.value+=1
        mutex_two.release()

def final_print():
    if "-l" in sys.argv:
        resume = "\n"+"Total de linhas com a palavra "+"'"+text+"'"+": "+str(total.value)+" linhas"
        print(resume)
    elif "-c" in sys.argv:
        resume = "\n"+"Total de ocorrências de "+"'"+text+"'"+" nos ficheiros "+str(files)+": "+str(total_words.value)+" vezes"
        print(resume)

########################### FINAL METODOS #######################################
        
signal.signal(signal.SIGINT, ctrl)      # SIGINT signal that triggers function ctrl

########################### INICIO DO PROGRAMA #######################################
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
        if not ".bin" in log_file:
            start+=1
            valid = False
            while not valid:
                log_file = input("Deseja indicar o nome do ficheiro bin (Se 'n' o ficheiro será Default.bin) (y/n): ")
                if log_file == "y":
                    log_file = input("Indique o nome do ficheiro bin (file.bin): ")
                    if not ".bin" in log_file:
                        valid = False
                    else:
                        valid = True
                elif log_file == "n":
                    log_file = "Default.bin"
                    valid = True
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

    ProcessPool = []
    for i in range(n_processes):
        p = Process(target=read_files, args=(i,))
        p.start()
        ProcessPool.append(p)

    time.sleep(0.5)
    
    for each in ProcessPool:
        each.join()
    
    duration = time.time() - duration  # calculates final duration of the whole program
    if "-f" in sys.argv:
        with open(log_file, 'ab') as handle:
            pickle.dump(time.strftime("%H:%M:%S:%ms", time.gmtime(duration)), handle, -1) # writes in the log file that same duration as seen above

    final_print()
    
else:
    print("Error: -c or -l must be included on the command line.")                  


########################### FINAL DO PROGRAMA #######################################
