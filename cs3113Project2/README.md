#cs3113-project2


##How to Build:
Create a Makefile for the main program. Need a main program to read name of the algoritim, total size of the structure, and the file name from the command line. Save the name of the algoritim and total size of structure to variables. Then to read the file, create char pointers that are assigned to request, list, available, release, find, and bestfit. When reading in the file make sure to ignore the '#' character.5 Then use strtok and strchamp to process each command. For example if it read in "request" then you will call a function that processes the request by passing in the process Name, the size of the process, and the alg name. 

##doRequest function 
Takes in three parameters: the char pointer of the process name, a long int of the  size of the process, and the char pointer of the alg name. This function goes through and compares the alg name to bestfit, firstfit, worstfit, and nextfit. Which ever name it matches to, you will call its corresponding function. For example if the alg name matched with "bestfit" you will cal algBestFitRequest(processname, sizeofprocess) 

##doRelease function 
Takes in one parameter which is the process name. This process "releases the memory held by a process A. On success, print FREE A n x where n is the amount of reclaimed memory and x is the starting relative address of the released memory. On error, print FAIL RELEASE A." 

##doFind function 
Takes in one parameter which is the process name. This process "rocates the starting address and size allocated by the process labeled A. If successful, this command returns a tuple , where  is the amount allocated by A and x is the relative starting address of the process labeled A. If unsuccessful, the program should print FAULT." 

##dolistAvaliable function 
Takes no parameters. This function scans the list to "print the location information for all available memory. Prints a list of space separated pairs of “  ”, where  is the amount memory available and  is the starting location. If there are no available blocks you should print FULL.

##dolistAssigned function 
takes no parameters. This function scanes the linked list to "Returns a list of space separated triples including of the form “  ”, where  represents process labels,  represents the number of allocated bytes for that process, and  is the relative starting address of the process. If there are no allocated blocks, this should print NONE." 

##algBestFitRequest function 
Takes the processName and size of process as parameters. This function performs the best-fit alg with a corner case of if multiple memory locations have the same “winning” size, I chosee the lowest open space as the winner. Best fit works by inserting the process in the smallest space space avaliable. 

##algWorstFitRequestion function 
Takes the processName and size of process as parameters. This function performs the worst-fit alg with a corner case of if multiple memory locations have the same “winning” size, I chosee the lowest open space as the winner. Worst fit works by inserting the process in the largest space space avaliable. 

##algFirstFit function 
Takes the processName and size of process as parameters. This function performs the first-fit alg in which it allocates the the process in the first open space avaliable that is big enough. 

##algNextFit function 
Takes the processName and size of process as parameters. This function performs the next-fit alg. 

How to Run: Create a test file with various commands like request, list avaliable, find, list assigned. Run program by using command "./project2 ALGNAME TOTALSIZEOFMEM testfile" to run the program 

Bugs: Gradescope wasn't working

Resources: Dr. Grant's Lecture on 11/8/22
