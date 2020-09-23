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

#define OPCODE_BUFFER_SIZE 	sizeof(unsigned char) * 50
#define STR_ReadBuffer 		sizeof(char) * 100

//////////////////////////////////////////////////////////////////////////////////


int main(int argc, char *argv[])
{

	//////////////////////////////////////////////////////////////////////////////////

	pid_t pid;
	off_t MemAddress;
	unsigned long ReadBuffer;

	int fd;
	char mFileName[50];
	size_t nByte;
	
	unsigned char OpcodeRead[OPCODE_BUFFER_SIZE];
	char* strBuffer = (char*) malloc(STR_ReadBuffer);	
	char tmpBuffer[50];

	memset(strBuffer, 0, STR_ReadBuffer);

	if (argc != 4)
	{
		printf("[*] Help\n");
		printf("[*] application [PID] [StartAddress] [Size]\n");
		exit(0);
	}

	pid 			= (unsigned long) atoi(argv[1]);
	MemAddress 		= strtoul(argv[2], NULL, 16);
	ReadBuffer 		= (unsigned long) atoi(argv[3]);

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

	lseek(fd, MemAddress, SEEK_SET);

	if ((nByte = read(fd, OpcodeRead, ReadBuffer)) <= 0 )
	{
		printf("Failed Read\n");
		return 0;
	}

	//////////////////////////////////////////////////////////////////////////////////

	strcat(strBuffer, tmpBuffer);

	for (int i=0; i<ReadBuffer; i++)
	{
		sprintf(tmpBuffer, "%02X ", OpcodeRead[i]);
		strcat(strBuffer, tmpBuffer);
	}

	//////////////////////////////////////////////////////////////////////////////////

	printf("%s\n", strBuffer);

//	ptrace(PTRACE_DETACH, pid, 0, 0);

	close(fd);
	free(strBuffer);

	return 0;

	//////////////////////////////////////////////////////////////////////////////////

}