Sistemas Operativos - Trabalho realizado por:
GRUPO 21
Ana Nunes nº 51596 LTI
Sofia Lourenço nº 54950 LTI
Inês Marcelino nº 54991 LTI

On file pgrepwc.py, the program is executed with processes.
On file pgrepwc_threads.py, the program is executed with threads.

NAME
pgrepwc and pgrepwc_threads - print lines and ocorrences in given files matching the indicated text

DESCRIPTION
pgrepwc and pgrepwc_threads searches input FILES (or standard input if no files are given) for lines containing a match with given TEXT.
	
PYTHON VERSION 3.8

SYNOPSIS
pgrepwc [-c|-l] text
pgrepwc [-c|-l] text {files}
pgrepwc [-c|-l] [-p n] text
pgrepwc [-c|-l] [-p n] text {files}


OPTIONS
pgrepwc
	pgrepwc, is required.
	pgrepwc = "pgrepwc".
	Defines the beginning of command line.
	If not given, program won't work properly.

-p n
	-p n, is optional.
	n = int. 
	Defines the number of parallel threads/processes that are used for searching.
	If this command is not given, only one thread/process will be used.	

[-c|-l]
	[-c|-l], one of them is required and can't be used at the same time.
	Doesn't have args.
	If -c is used, defines the total ocorrences in given files matching the indicated text.
	If -l is used, defines the total lines in given files matching the indicated text.
	If one of those is not given, an error occures.

TEXT
	TEXT, is required.
	TEXT = str.
	Defines a string to search from files.
	If not given, program won't work properly.


