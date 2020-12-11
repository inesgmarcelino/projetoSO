import os
import sys
from multiprocessing import Pool,Queue,Value
from multiprocessing import Process
import threading
from sys import argv
from sys import stdin
import time
import signal
import pickle

dicProc={}
log_file = sys.argv[1]
read_file =open(log_file, "rb")
date = pickle.load(read_file)
print("Inicio da execucao da pesquisa: "+str(date)) # gets de datetime
control = True
while control:
    try:
        y = pickle.load(read_file)   
        if type(y) != str :
            if y[0] not in dicProc: #if os.getpid not in dicproc
                dicProc[y[0]] = [y[1:]] #includes the os.getpid on the key, and then adds the items specific to that pid to dic
            else:
                dicProc[y[0]].append(y[1:]) #appends the items for the specific pid on dic
        else:
            print("Duracao da Execucao: "+str(y))  # gets the time
    except:
        control=False

for process in dicProc:
        print ("Processo: "+str(process))
        for job in dicProc[process]:
                print ("\tficheiro: "+str(job[0]))
                print ("\t\ttempo de pesquisa: "+str(job[1]))
                print ("\t\tdimensao do ficheiro: "+str(job[2]))
                if str(job[4]) == "-c":
                    print ("\t\tnumero de ocorrencias: "+str(job[3]))
                elif str(job[4]) == "-l":
                    print ("\t\tnumero de linhas: "+str(job[3]))






