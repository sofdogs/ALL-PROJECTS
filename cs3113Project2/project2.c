
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <errno.h>

struct memAllocation {
    char processName[17]; //c strings terminated w \0
    long int size;
    long int startPos;
    struct memAllocation * next;
};

struct memAllocation * g_memAllocationList = NULL;
struct memAllocation * g_nextFit = NULL;
long int totalMemory = 0;


//anoter var where i was last or nextfir inserted
void algBestFitRequest(char*processName, long int sizeOfProcess)
{
    long int bestFreeSpace = totalMemory + 1;
    //allocates chunk of memory
    struct memAllocation* memAlloc = (struct memAllocation*)malloc (sizeof (struct memAllocation)); //creating my list
    strcpy (memAlloc->processName, processName);
    memAlloc->size = sizeOfProcess;
    memAlloc->next = NULL;
    //startpos depends where we insert in list

    if (g_memAllocationList == NULL)
    {
        if(sizeOfProcess< totalMemory)
        {
            g_memAllocationList = memAlloc;
            memAlloc->startPos = 0;
            memAlloc->next = NULL;
            printf ("ALLOCATED %s %ld\n", memAlloc->processName, memAlloc->startPos);
        } else {
            printf ("FAIL REQUEST %s %ld\n", memAlloc->processName, memAlloc->size);
            free (memAlloc);
        }
       
    }
    else
    {
        struct memAllocation* ma = g_memAllocationList; //our global var start at 0
        struct memAllocation* bestCurrBlock = NULL;
        if (ma->startPos != 0)
        {
            long int freeSpace = ma->startPos;
            if (freeSpace >= sizeOfProcess && freeSpace < bestFreeSpace)//if we already found a space use first one
            {
                bestFreeSpace = freeSpace;
                bestCurrBlock = ma; //block before insertion
            }
        }
        while (ma != NULL)
        {
            long int endPos = ma->startPos + ma->size;
            if (ma->next != NULL)
            {
                struct memAllocation* nextBlock = ma->next;
                long int freeSpace = nextBlock->startPos - endPos;
                //see if next address is equal to your current one
                if (freeSpace >= sizeOfProcess && freeSpace < bestFreeSpace)//if we already found a space use first one
                {
                    bestFreeSpace = freeSpace;
                    bestCurrBlock = ma; //block before insertion
                }

            }
            else
            {
                long int freeSpace = totalMemory - endPos;

                if (freeSpace >= sizeOfProcess && freeSpace < bestFreeSpace)//if we already found a space use first one
                {
                    bestFreeSpace = freeSpace;
                    bestCurrBlock = ma; //block before insertion
                }
            }
            ma = ma->next;
        }
        //fail condition
        if (bestCurrBlock == NULL)
        {
            printf ("FAIL REQUEST %s %ld\n", memAlloc->processName, memAlloc->size);
            free (memAlloc);
        }
        else
        {
            if (bestCurrBlock == g_memAllocationList && bestCurrBlock->startPos != 0)
            {
                g_memAllocationList = memAlloc;
                memAlloc->startPos = 0;
                memAlloc->next = bestCurrBlock;
            }
            else
            {
                memAlloc->startPos = bestCurrBlock->startPos + bestCurrBlock->size;
                memAlloc->next = bestCurrBlock->next; //set new block to addy of c
                bestCurrBlock->next = memAlloc;
            }

            printf ("ALLOCATED %s %ld\n", memAlloc->processName, memAlloc->startPos);
        }
    }
}

void algFirstFitRequest(char*processName, long int sizeOfProcess)
{
    int isFull = 0;

    //allocates chunk of memory
    struct memAllocation* memAlloc = (struct memAllocation*)malloc (sizeof (struct memAllocation));
    strcpy (memAlloc->processName, processName);
    memAlloc->size = sizeOfProcess;
    memAlloc->next = NULL;
    //startpos depends where we insert in list

    if (g_memAllocationList == NULL)
    {
        if (sizeOfProcess <= totalMemory)
        {
            g_memAllocationList = memAlloc;
            memAlloc->startPos = 0;
            memAlloc->next = NULL;
        }
        else
        {
            isFull = 1; // not enough room
        }
    }
    else
    {
        struct memAllocation* currBlock = g_memAllocationList; //our global var

        // check for free space at the very top...
        if (currBlock->startPos != 0)
        {
            long int freeSpace = currBlock->startPos;
            if (freeSpace >= sizeOfProcess)
            {
                memAlloc->startPos = 0;
                memAlloc->next = currBlock;

                // set as the new first block...
                g_memAllocationList = memAlloc;
                printf ("ALLOCATED %s %ld\n", memAlloc->processName, memAlloc->startPos);
                return;
            }
        }

        while (currBlock != NULL)
        {
            //how much of a gab between current and next that was allocated, how much space
            //end = start + size
            long int endPos = currBlock->startPos + currBlock->size;
            if (currBlock->next != NULL)
            {
                //getting startPos of next mem block that was allocated
                struct memAllocation* nextBlock = currBlock->next;
                long int freeSpace = nextBlock->startPos - endPos;
                //this is requested size
                if (freeSpace >= sizeOfProcess)
                {
                    //to set this start and next
                    memAlloc->startPos = endPos;
                    //block a now pointing to c
                    currBlock->next = memAlloc;
                    //c now points to b
                    memAlloc->next = nextBlock;
                    break;
                }
            }
            else
            {
                //if at end of list
                long int freespace = totalMemory - endPos;  //how much free space is left
                //if enogu space to satify request
                if (freespace >= sizeOfProcess)
                {
                    // link currBlock to the new block...
                    currBlock->next = memAlloc;

                    // set his start and next
                    memAlloc->startPos = endPos;
                    memAlloc->next = NULL;  //end of list so should be null
                    break;
                }
                else
                {
                    isFull = 1;
                }
            }

            //to go to next item
            currBlock = currBlock->next;
        }
    }

    if (isFull == 1)
    {
        printf ("FAIL REQUEST %s %ld\n", processName, sizeOfProcess);
        free (memAlloc);
    }
    else
    {
        printf ("ALLOCATED %s %ld\n", memAlloc->processName, memAlloc->startPos);
    }

}

void algWorstFitRequest(char*processName, long int sizeOfProcess)
{
    long int bestFreeSpace = 0;
    //allocates chunk of memory
    struct memAllocation * memAlloc =(struct memAllocation*)malloc(sizeof(struct memAllocation)); //creating my list
    strcpy (memAlloc->processName, processName);
    memAlloc->size = sizeOfProcess;
    memAlloc->next = NULL;
    //startpos depends where we insert in list

    if(g_memAllocationList == NULL)
    {
        if(sizeOfProcess<= totalMemory)
        {
            g_memAllocationList = memAlloc;
            memAlloc-> startPos = 0;
            memAlloc-> next = NULL;
            printf("ALLOCATED %s %ld\n", memAlloc->processName, memAlloc->startPos);
        } else {
            printf("FAIL REQUEST %s %ld\n", memAlloc->processName, memAlloc->size);
            free(memAlloc);
            return;
        }
    } else
    {
        struct memAllocation* ma = g_memAllocationList; //our global var start at 0
        struct memAllocation* bestCurrBlock = NULL;

        if(ma->startPos!=0)
        {
            long int freeSpace = ma->startPos;
            if(freeSpace >= sizeOfProcess && freeSpace > bestFreeSpace)//if we already found a space use first one
            {
                bestFreeSpace = freeSpace;

                bestCurrBlock = ma; //block before insertion
                 
            }
        }
        while(ma != NULL)
        {
            long int endPos = ma->startPos + ma->size;
            if(ma->next!=NULL)
            {
                struct memAllocation*nextBlock = ma -> next;
                long int freeSpace = nextBlock->startPos - endPos;
                //see if next address is equal to your current one
                if(freeSpace >= sizeOfProcess && freeSpace > bestFreeSpace)//if we already found a space use first one
                {
                   bestFreeSpace = freeSpace;

                   bestCurrBlock = ma; //block before insertion
                }

            } else {
                long int freeSpace = totalMemory - endPos;

                if(freeSpace >= sizeOfProcess && freeSpace > bestFreeSpace)//if we already found a space use first one
                {
                   bestFreeSpace = freeSpace;

                   bestCurrBlock = ma;
                }

            }
            ma = ma->next;
        }
        //fail condition
        if(bestCurrBlock==NULL)
        {
             printf("FAIL REQUEST %s %ld\n", memAlloc->processName, memAlloc->size);
             free(memAlloc);
        } else {
            if (bestCurrBlock == g_memAllocationList && bestCurrBlock->startPos != 0)
            {
                g_memAllocationList = memAlloc;
                memAlloc->startPos = 0;
                memAlloc->next = bestCurrBlock;
            }
            else
            {
                memAlloc->startPos = bestCurrBlock->startPos + bestCurrBlock->size;
                memAlloc->next = bestCurrBlock->next; //set new block to addy of c
                bestCurrBlock->next = memAlloc;
            }
            printf("ALLOCATED %s %ld\n", memAlloc->processName, memAlloc->startPos);
               
        }
    }
}

void algNextFitRequest(char*processName, long int sizeOfProcess)
{
    int isFull = 0;

    //allocates chunk of memory
    struct memAllocation* memAlloc = (struct memAllocation*)malloc (sizeof (struct memAllocation));
    strcpy (memAlloc->processName, processName);
    memAlloc->size = sizeOfProcess;
    memAlloc->startPos = 0;
    memAlloc->next = NULL;
    //startpos depends where we insert in list

    if (g_nextFit == NULL)
    {
        if (sizeOfProcess <= totalMemory)
        {
            g_nextFit = memAlloc;
            g_memAllocationList = memAlloc;
            memAlloc->startPos = 0;
            memAlloc->next = NULL;
        }
        else
        {
            isFull = 1;
        }
    }
    else
    {
        struct memAllocation* currBlock = g_nextFit; //our global var
        int timesThruLoop = 0;

        while (currBlock != g_nextFit || timesThruLoop <= 2) //a way to enter loop for first time
        {
            ++timesThruLoop;

            long int endPos = currBlock->startPos + currBlock->size;

            if (currBlock->next != NULL)
            {
                //getting startPos of next mem block that was allocated
                struct memAllocation* nextBlock = currBlock->next;
                long int freeSpace = nextBlock->startPos - endPos;
                //this is requested size
                if (freeSpace >= sizeOfProcess)
                {
                    //to set this start and next
                    memAlloc->startPos = endPos;
                    //block a now pointing to c
                    currBlock->next = memAlloc;
                    //c now points to b
                    memAlloc->next = nextBlock;
                    g_nextFit = memAlloc;
                    break;
                }
            }
            else
            {
                //if at end of list
                long int freespace = totalMemory - endPos;  //how much free space is left
                //if enogu space to satify request
                if (freespace >= sizeOfProcess)
                {
                    memAlloc->startPos = endPos;
                    memAlloc->next = NULL;
                    currBlock->next = memAlloc;
                    g_nextFit = memAlloc;
                    break;
                }
                else
                {
                    isFull = 1;
                }
            }

            //to go to next item
            currBlock = currBlock->next;

            if (currBlock == NULL) //end of our list
            {
                currBlock = g_memAllocationList; //reset it to the top of list

                //check for gap at very top of heap
                if (g_memAllocationList->startPos != 0)
                {
                    long int freeSpace = currBlock->startPos;
                    if (freeSpace >= sizeOfProcess)
                    {
                        memAlloc->startPos = 0;
                        memAlloc->next = g_memAllocationList;

                        g_memAllocationList = memAlloc; // becomes the new start of list
                        printf ("ALLOCATED %s %ld\n", memAlloc->processName, memAlloc->startPos);
                        return;
                    }
                }
            }
        }
    }

    if (isFull == 1)
        printf ("FAIL REQUEST %s %ld\n", memAlloc->processName, memAlloc->size);
    else
        printf ("ALLOCATED %s %ld\n", memAlloc->processName, memAlloc->startPos);
}


void dorequest(char*processName, long int sizeOfProcess, char*algName)
{
    //printf("do request: %s %ld %s\n", processName,sizeOfProcess, algName);
    if(strcmp(algName, "BESTFIT") ==0)
        algBestFitRequest(processName, sizeOfProcess);

    else if(strcmp(algName, "FIRSTFIT") ==0)
        algFirstFitRequest(processName, sizeOfProcess);

    else if(strcmp(algName, "WORSTFIT") ==0)
        algWorstFitRequest(processName, sizeOfProcess);

    else if(strcmp(algName, "NEXTFIT") ==0)
        algNextFitRequest(processName, sizeOfProcess);
}

void doRelease(char*processName)
{
    struct memAllocation* currBlock = g_memAllocationList; //i variable
    struct memAllocation* prevBlock = NULL;

    while(currBlock != NULL)//iterate
    {
        //found correct block to remove
        if(strcmp(processName, currBlock->processName)==0)
        {
            //first block case
            if(currBlock == g_memAllocationList)//first block in list
            {
                g_memAllocationList = currBlock -> next; //next block
            }
            //last block
            else if(currBlock->next == NULL)
            {
                prevBlock->next = NULL;

            } else
            {
                prevBlock->next = currBlock->next; //gets c block
            }
            printf("FREE %s %ld %ld\n", processName, currBlock->size, currBlock->startPos);
            if(g_nextFit == currBlock)
            {
                g_nextFit = prevBlock;
            }
            free(currBlock);
            return; //if we find block then get out
        }

        prevBlock = currBlock;
        currBlock = currBlock -> next; //i++
    }

    printf("FAIL RELEASE %s\n", processName);

}

void doFind(char*processName)
{
    struct memAllocation* currBlock = g_memAllocationList; //i variable
    while (currBlock != NULL)
    {
        if (strcmp (processName, currBlock->processName) == 0)
        {
            printf ("(%s, %ld, %ld)\n", processName, currBlock->size, currBlock->startPos);
            return;
        }

        currBlock = currBlock->next;
    }
    printf ("FAULT\n");
    //  printf("do find:  %s\n", processName);
}

void dolistAvaliable()
{
    int hasSpace = 0;
    if (g_memAllocationList == NULL) //no request made so all mem avaliable
    {
        hasSpace = 1;
        printf ("(%ld, %d) ", totalMemory, 0);
    }
    else
    {
        if (g_memAllocationList != NULL && g_memAllocationList->startPos != 0)
        {
            hasSpace = 1;
            printf ("(%ld, %d) ", g_memAllocationList->startPos, 0);
        }

        //iterate link list
        struct memAllocation* currBlock = g_memAllocationList; //our global var

        while (currBlock != NULL)
        {
            long int endPos = currBlock->startPos + currBlock->size;
            struct memAllocation* nextBlock = currBlock->next; //going to next field can be block or null
            if (nextBlock == NULL)
            {
                long int freeSpace = totalMemory - endPos;
                if (freeSpace)
                {
                    printf ("(%ld, %ld) ", freeSpace, endPos);
                    hasSpace = 1;
                }
            }
            else
            {
                long int freespace = nextBlock->startPos - endPos;

                if (freespace != 0)
                {
                    printf ("(%ld, %ld) ", freespace, endPos); //free space and start
                    hasSpace = 1;
                }
            }
            //go to next block
            currBlock = currBlock->next; //sets variable to next memory allocation
        }
    }

    if (hasSpace == 0)
    {
        printf ("FULL");
    }
 
    printf ("\n");
}

void dolistAssigned ()
{
    if (g_memAllocationList == NULL)
    {
        printf ("NONE\n");
    }
    else
    {
        //iterate link list
        struct memAllocation* ma = g_memAllocationList; //our global var
        while (ma != NULL)
        {
            //to go to next item
            printf ("(%s, %ld, %ld) ", ma->processName, ma->size, ma->startPos);
            ma = ma->next;
        }
        printf ("\n");
    }
}



int main (int argc, char* argv[])
{
    //values to read from stdin
    char* algName = NULL;
    FILE* fp = NULL; //third
    char ch;
    char* fileName;

    //reading in algName
    if (argc > 1)
    {
        algName = argv[1];
        ///printf("%s\n", algName);
    }
    
    //if (!(strcmp (algName, "BESTFIT") == 0 || strcmp (algName, "WORSTFIT") == 0))
    //    return 0;
    
    //reading in interger SIZE OF MEMORY
    totalMemory = atoi (argv[2]);

    char line[100];
    char* value;
    char* value2;

    char* request = "REQUEST";
    char* LIST = "LIST";
    char* AVAILABLE = "AVAILABLE";
    char* RELEASE = "RELEASE";
    char* FIND = "FIND";
    char* BESTFIT = "BESTFIT";

    char* delim = " \n";
    if (argc > 1)
    {
        fp = fopen (argv[3], "r");
        //file DNE
        if (fp == NULL)
        {
            fprintf (stderr, "file DNE");
            return -1; //error condition
        }
        //fprintf(stderr, "arg 1 = %s\n", argv[3]);
    }

    while (fgets (line, sizeof (line), fp) != NULL)
    {
        if (strchr (line, '#') != NULL)
        {
            continue;
        }

        value = strtok (line, delim);
        if (strcmp (value, request) == 0)
        {

            char* processName = strtok (NULL, delim);

            char* processSize = strtok (NULL, delim);
            long int sizeOfProcess = atol (processSize);
            //printf("memory: %s\n" , processSize);

            dorequest (processName, sizeOfProcess, algName);
        }

        if (strcmp (value, LIST) == 0)
        {
            value2 = strtok (NULL, delim);


            //printf("command: %s\n" , value2);

            //printf("command: %s\n" , value);
            //if it's not availabe it will be assigned
            if (strcmp (value2, "AVAILABLE") == 0)
            {
                //printf("test");
                dolistAvaliable ();
            }
            else
            {

                dolistAssigned ();

            }

        }

        if (strcmp (value, RELEASE) == 0)
        {
            char* processName = strtok (NULL, delim);
            doRelease (processName);
        }

        if (strcmp (value, FIND) == 0)
        {
            char* processName = strtok (NULL, delim);
            doFind (processName);
        }

    }

    exit (EXIT_SUCCESS);
}




