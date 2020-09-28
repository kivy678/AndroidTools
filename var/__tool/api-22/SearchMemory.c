#define _GNU_SOURCE
#define _LARGEFILE64_SOURCE

//////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <sys/ptrace.h>
#include <sys/wait.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define OPCODE_BUFFER_SIZE 	sizeof(unsigned char) * 5
#define STR_BUFFER_SIZE 	sizeof(char) * 200

//////////////////////////////////////////////////////////////////////////////////

int CodeCompare(unsigned long, unsigned char [], unsigned char []);
void PathDataParser(char*, unsigned long, unsigned char []);

//////////////////////////////////////////////////////////////////////////////////


int main(int argc, char *argv[])
{

	//////////////////////////////////////////////////////////////////////////////////

	pid_t pid;
	off_t StartAddress;
	off_t EndAddress;
	unsigned long SearchSize;

	int fd;
	char mFileName[50] = {0};
	size_t nByte;
	
	char* strBuffer = (char*) malloc(STR_BUFFER_SIZE);
	char tmpBuffer[50] = {0};

	memset(strBuffer, 0, STR_BUFFER_SIZE);

	unsigned char OpcodeRead[OPCODE_BUFFER_SIZE] = {0};
	unsigned char OpcodeSearch[OPCODE_BUFFER_SIZE] = {0};

	if (argc != 6)
	{
		printf("[*] Help\n");
		printf("[*] application [PID] [Start Address] [End Address] [Search Size] [Search Data]\n");
		exit(0);
	}

	pid 			= (unsigned long) atoi(argv[1]);
	StartAddress 	= strtoul(argv[2], NULL, 16);
	EndAddress 		= strtoul(argv[3], NULL, 16);
	SearchSize 		= (unsigned long) atoi(argv[4]);

	PathDataParser(argv[5], SearchSize, OpcodeSearch);

	//////////////////////////////////////////////////////////////////////////////////

	sprintf(mFileName, "/proc/%d/mem", pid);

	if ((fd = open(mFileName, O_RDWR | O_LARGEFILE)) == -1)
	{
		printf("Failed Open Mem\n");
	}
/*
	if (ptrace(PTRACE_ATTACH, pid, 0, 0) < 0)
	{
		printf("Ptrace Attach Failed\n");

		free(strBuffer);
		return 0;
	}

	waitpid(pid, NULL, WUNTRACED);
*/	
	//////////////////////////////////////////////////////////////////////////////////

	while (StartAddress < EndAddress)
	{
		lseek(fd, StartAddress, SEEK_SET);

		if ((nByte = read(fd, OpcodeRead, SearchSize)) == -1 )
		{
			//printf("Failed Read\n");
			break;
		}
		else
		{	
			if (CodeCompare(SearchSize, OpcodeRead, OpcodeSearch) > 0)
			{
				sprintf(tmpBuffer, "0x%08lX\n", StartAddress);
				strcat(strBuffer, tmpBuffer);
			}

			StartAddress += 1;
		}

	}
	
	//////////////////////////////////////////////////////////////////////////////////

	printf("%s", strBuffer);

//	ptrace(PTRACE_DETACH, pid, 0, 0);

	close(fd);
	free(strBuffer);

	return 0;

	//////////////////////////////////////////////////////////////////////////////////
}


int CodeCompare(unsigned long SearchSize, unsigned char OpcodeRead[], unsigned char OpcodeSearch[])
{
	for (int i=0; i<SearchSize; i++)
	{
		if (OpcodeRead[i] != OpcodeSearch[i])
			return -1;
	}

	return 1;
}


void PathDataParser(char* data, unsigned long SearchSize, unsigned char buffer[])
{
	char tmpBuffer[5] = {0};

	for (int i=0; i<SearchSize; i++)
	{
		sprintf(tmpBuffer, "0x%c%c", *(data+(i*2)), *(data+(i*2)+1));
		buffer[i] = strtoul(tmpBuffer, NULL, 16);
	}

}
