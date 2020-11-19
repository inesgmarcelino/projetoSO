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
pgrepwc [-c|-l] [-a s] text
pgrepwc [-c|-l] [-a s] text {files}
pgrepwc [-c|-l] [-f file] text
pgrepwc [-c|-l] [-f file] text {files}
pgrepwc [-c|-l] [-p n] [-a s] text
pgrepwc [-c|-l] [-p n] [-a s] text {files}
pgrepwc [-c|-l] [-p n] [-f file] text
pgrepwc [-c|-l] [-p n] [-f file] text {files}
pgrepwc [-c|-l] [-a s] [-f file] text
pgrepwc [-c|-l] [-a s] [-f file] text {files}
pgrepwc [-c|-l] [-p n] [-a s] [-f file] text
pgrepwc [-c|-l] [-p n] [-a s] [-f file] text {files}


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

-a s
	-a s, is optional.
	s = int. 
	Defines the time interval parent process has to write to stdout the counting status.
	That status gives the info of the number of occurrences of the word indicated or of 
	the lines where the word was found at the moment, the number of files completely 
	processed, and the time that has occurred since program execution has started.
	#If this command is not given, only one thread/process will be used.# -- usar?	

-f file
	-f file, is optional.
	file = str. 
	Defines the file used to save the program execution history.
	The contents of the file must be stored in binary.
	The information stored in this file should be the information that is required 
	for the hgrepwc command.	-- devemos dizer isto?

TEXT
	TEXT, is required.
	TEXT = str.
	Defines a string to search from files.
	If not given, program won't work properly.

################################## hpgrepwc ##################################

NAME
hpgrepwc - read the excutation history of pgrepwc program

DESCRIPTION
read the excution history of pgrepwc program saved in file and shows that info in to stdout. -- devemos apresentar o formato do stdout?
	
PYTHON VERSION 3.8

SYNOPSIS
hgrepwc {file}