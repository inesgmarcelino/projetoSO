import os
import sys
from multiprocessing import Queue,Value
from sys import argv
from sys import stdin
from threading import Thread
import time
import argparse
import re
                                                                  


###################### THREADING ########################### 

global qFiles
qFiles = []

def read_files(ind):                         # main function: reads file and prints all the lines with the specific text indicated on command line
    """
    Thread read files

    Requires:
    - ind, an int of the specific thread;
    Ensures:
    - prints lines where the word is indicated \
      and the number of ocurrences of the word in individual files.
    """
    while position.value < len(qFiles):      # While the value of position is less that len of list qFiles
        file =  qFiles[position.value]       # position.value is the position of list qFiles
        position.value+=1                    # the position of list qFiles is increased

        read_file = open(file, "r")
        lines = []

        total_words_on_individual_file = 0                  # Variable value with the sum of the word in individual files

##        print("Thread ["+str(ind)+"]")
        for line in read_file:
            result = re.sub("[^\w]", " ", line).split()     # Replaces inside the line characters there arent alphanumeric with spaces. [^\w] - not alphanumeric 
            
            if text in result:
##                print("Thread ["+str(ind)+"]",read_file.name, "linha ----> ", line)
                lines.append(line.split())
                
                total.value+=1
                total_word.value = result.count(text)                           
                total_words.value += total_word.value                           
                total_words_on_individual_file += total_word.value
                time.sleep(0.2)
        print("\n---------",read_file.name,"---------\n")
        for words in lines:
            print(" ".join(words))
        print("\nocorrências de "+"'"+text+"'"+" no ficheiro "+read_file.name+" : "+str(total_words_on_individual_file))

        read_file.close()

total = Value("i",0)                    
total_word = Value("i",0)                        
total_words = Value("i", 0)                      
position = Value("i",0)                      # Variable value for the position of list qFiles

my_parser = argparse.ArgumentParser()        # Add the arguments so it can automatically create -h and the -c | -l

text = ""

# Adicionar -a e -f
if ("-p" in sys.argv and "-c" in sys.argv and "-a" in sys.argv and "-f" in sys.argv) or ("-p" in sys.argv and "-l" in sys.argv and "-a" in sys.argv and "-f" in sys.argv):
    n_processes = sys.argv[sys.argv.index("-p")+1]
    my_parser.add_argument(dest=text, metavar="text", type=str)
    
    if not n_processes.isdigit():
        raise("Number of processes must be an integer.")
    else:
        n_processes = int(n_processes)
    start = 5
    
elif ("-p" not in sys.argv and "-c" in sys.argv and "-a" in sys.argv and "-f" in sys.argv) or ("-p" not in sys.argv and "-l" in sys.argv and "-a" in sys.argv and "-f" in sys.argv):
    n_processes = 1
    start = 3
    my_parser.add_argument(dest=text, metavar="text", type=str)

elif ("-p" not in sys.argv and "-c" not in sys.argv and "-a" in sys.argv and "-f" in sys.argv) or ("-p" not in sys.argv and "-l" not in sys.argv and "-a" in sys.argv and "-f" in sys.argv): # for argparse add_mutually_exclusive_group error \
    start = 2                                                                                            # to work even when not -p -c and -l on command line

elif ("-p" in sys.argv and "-c" not in sys.argv and "-a" in sys.argv and "-f" in sys.argv) or ("-p" in sys.argv and "-l" not in sys.argvand "-a" in sys.argv and "-f" in sys.argv):         # for argparse argparse add_mutually_exclusive_group error \
    start = 4                                                                                            # to work even when not -c or -l on command line
    
elif("-p" in sys.argv and "-c" in sys.argv and "-a" not in sys.argv and "-f" in sys.argv) or ("-p" in sys.argv and "-l" in sys.argv and "-a" not in sys.argv and "-f" in sys.argv):
    n_processes = sys.argv[sys.argv.index("-p")+1]
    my_parser.add_argument(dest=text, metavar="text", type=str)
    if not n_processes.isdigit():
        raise("Number of processes must be an integer.")
    else:
        n_processes = int(n_processes)
    start = 5
elif ("-p" not in sys.argv and "-c" in sys.argv and "-a" not in sys.argv and "-f" in sys.argv) or ("-p" not in sys.argv and "-l" in sys.argv and "-a" not in sys.argv and "-f" in sys.argv):
    n_processes = 1
    start = 3
    my_parser.add_argument(dest=text, metavar="text", type=str)

elif ("-p" not in sys.argv and "-c" not in sys.argv and "-a" not in sys.argv and "-f" in sys.argv) or ("-p" not in sys.argv and "-l" not in sys.argv and "-a" not in sys.argv and "-f" in sys.argv): # for argparse add_mutually_exclusive_group error \
    start = 2                                                                                            # to work even when not -p -c -a and -l on command line

elif ("-p" in sys.argv and "-c" not in sys.argv and "-a" not in sys.argv and "-f" in sys.argv) or ("-p" in sys.argv and "-l" not in sys.argvand "-a" not in sys.argv and "-f" in sys.argv):         # for argparse argparse add_mutually_exclusive_group error \
    start = 4                                                                                            # to work even when not -c or -l on command line
elif ("-p" in sys.argv and "-c" in sys.argv and "-a" in sys.argv and "-f" not in sys.argv) or ("-p" in sys.argv and "-l" in sys.argv and "-a" in sys.argv and "-f" not in sys.argv):
    n_processes = sys.argv[sys.argv.index("-p")+1]
    my_parser.add_argument(dest=text, metavar="text", type=str)
    
    if not n_processes.isdigit():
        raise("Number of processes must be an integer.")
    else:
        n_processes = int(n_processes)
    start = 5
    
elif ("-p" not in sys.argv and "-c" in sys.argv and "-a" in sys.argv and "-f" not in sys.argv) or ("-p" not in sys.argv and "-l" in sys.argv and "-a" in sys.argv and "-f" not in sys.argv):
    n_processes = 1
    start = 3
    my_parser.add_argument(dest=text, metavar="text", type=str)

elif ("-p" not in sys.argv and "-c" not in sys.argv and "-a" in sys.argv and "-f" not in sys.argv) or ("-p" not in sys.argv and "-l" not in sys.argv and "-a" in sys.argv and "-f" not in sys.argv): # for argparse add_mutually_exclusive_group error \
    start = 2                                                                                            # to work even when not -p -c and -l on command line

elif ("-p" in sys.argv and "-c" not in sys.argv and "-a" in sys.argv and "-f" not in sys.argv) or ("-p" in sys.argv and "-l" not in sys.argvand "-a" in sys.argv and "-f" not in sys.argv):         # for argparse argparse add_mutually_exclusive_group error \
    start = 4                                                                                            # to work even when not -c or -l on command line
    
elif("-p" in sys.argv and "-c" in sys.argv and "-a" not in sys.argv and "-f" not in sys.argv) or ("-p" in sys.argv and "-l" in sys.argv and "-a" not in sys.argv and "-f" not in sys.argv):
    n_processes = sys.argv[sys.argv.index("-p")+1]
    my_parser.add_argument(dest=text, metavar="text", type=str)
    if not n_processes.isdigit():
        raise("Number of processes must be an integer.")
    else:
        n_processes = int(n_processes)
    start = 5
elif ("-p" not in sys.argv and "-c" in sys.argv and "-a" not in sys.argv and "-f" not in sys.argv) or ("-p" not in sys.argv and "-l" in sys.argv and "-a" not in sys.argv and "-f" not in sys.argv):
    n_processes = 1
    start = 3
    my_parser.add_argument(dest=text, metavar="text", type=str)

elif ("-p" not in sys.argv and "-c" not in sys.argv and "-a" not in sys.argv and "-f" not in sys.argv) or ("-p" not in sys.argv and "-l" not in sys.argv and "-a" not in sys.argv and "-f" not in sys.argv): # for argparse add_mutually_exclusive_group error \
    start = 2                                                                                            # to work even when not -p -c -a and -l on command line

elif ("-p" in sys.argv and "-c" not in sys.argv and "-a" not in sys.argv and "-f" not in sys.argv) or ("-p" in sys.argv and "-l" not in sys.argvand "-a" not in sys.argv and "-f" not in sys.argv):         # for argparse argparse add_mutually_exclusive_group error \
    start = 4

text = sys.argv[start]                # Index where text is
files = sys.argv[start+1:]            # Index where files are given, right after the text index

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
        qFiles.append(file)

elif len(files) != 0:
    for i in files:
        my_parser.add_argument(dest=i)             # argument of files
        qFiles.append(i)

group = my_parser.add_mutually_exclusive_group(required=True)
group.add_argument("-c", action="store_true")      # empty argument
group.add_argument("-l", action="store_true")      # empty argument
my_parser.add_argument("-p")
my_parser.add_argument("-a")
my_parser.add_argument("-f")
my_parser.add_argument(dest=text, metavar="text", type=str)

args = my_parser.parse_args()                      # Execute the parse_args() method

threadPool = []
for i in range(n_processes):                       # Create threads within range of n_processes, and start each thread with target function read_files
    p = Thread(target=read_files, args=(i,))
    p.start()
    threadPool.append(p)

for each in threadPool:
    each.join()

if "-l" in sys.argv:
    resume = "\n"+"Total de linhas com a palavra "+"'"+text+"'"+": "+str(total.value)+" linhas"
    print(resume)
elif "-c" in sys.argv:
    resume = "\n"+"Total de ocorrências de "+"'"+text+"'"+" nos ficheiros "+str(files)+": "+str(total_words.value)+" vezes"
    print(resume)




##################### END THREADING #########################
