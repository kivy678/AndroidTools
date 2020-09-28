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

//////////////////////////////////////////////////////////////////////////////////

#define BUFFER_SIZE 		16
#define STR_BUFFER_SIZE 	sizeof(char) * 5000

//////////////////////////////////////////////////////////////////////////////////


int main(int argc, char *argv[])
{

	//////////////////////////////////////////////////////////////////////////////////

	pid_t pid;
	off_t MemStartAddr;
	unsigned long PrintRow;
	off_t MemAddress;
	
	int fd;
	char mFileName[50] = {0};
	size_t nByte;

	char tmpBuffer[50] = {0};
	char* strBuffer = (char*) malloc(STR_BUFFER_SIZE);
	memset(strBuffer, 0, STR_BUFFER_SIZE);

	if (argc != 4)
	{
		printf("[*] Help\n");
		printf("[*] application [PID] [StartAddress] [Print Row]\n");
		exit(0);
	}

	pid 			= (unsigned long) atoi(argv[1]);
	MemStartAddr 	= strtoul(argv[2], NULL, 16);
	PrintRow 		= (unsigned long) atoi(argv[3]);
	MemAddress		= MemStartAddr;

	strcpy(strBuffer, "===================================================================================\n"
					  "Offset\t\t00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15   ASCII\n"
					  "===================================================================================\n");

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

	int	cnt = 1;
	unsigned char buffer[BUFFER_SIZE+1] = {0};
	
GET_BIN:
	lseek(fd, MemAddress, SEEK_SET);

	if ((nByte = read(fd, buffer, BUFFER_SIZE)) == -1 )
	{
		printf("Failed Read\n");
		return 0;
	}

	//////////////////////////////////////////////////////////////////////////////////

	sprintf(tmpBuffer, "0x%08lX\t", MemAddress);
	strcat(strBuffer, tmpBuffer);

	for (int i=0; i<BUFFER_SIZE; i++)
	{
		sprintf(tmpBuffer, "%02X ", buffer[i]);
		strcat(strBuffer, tmpBuffer);
	}

	strcat(strBuffer, "  ");

	for (int i=0; i<BUFFER_SIZE; i++)
	{
		sprintf(tmpBuffer, "%c", buffer[i]);
		strcat(strBuffer, tmpBuffer);
	}

	strcat(strBuffer, "\n");

	if (cnt < PrintRow)
	{
		MemAddress += BUFFER_SIZE;
		cnt += 1;
		goto GET_BIN;
	}

	//////////////////////////////////////////////////////////////////////////////////

	printf("%s\n", strBuffer);

//	ptrace(PTRACE_DETACH, pid, 0, 0);

	close(fd);
	free(strBuffer);

	return 0;

	//////////////////////////////////////////////////////////////////////////////////

}