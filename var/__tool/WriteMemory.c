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

#define OPCODE_BUFFER_SIZE 	sizeof(char) * 50
#define STR_BUFFER_SIZE 	sizeof(char) * 200

//////////////////////////////////////////////////////////////////////////////////


void PathDataParser(char* data, unsigned long PathSize, unsigned char buffer[])
{
	char tmpBuffer[5];

	for (int i=0; i<PathSize; i++)
	{
		sprintf(tmpBuffer, "0x%c%c", *(data+(i*2)), *(data+(i*2)+1));
		buffer[i] = strtoul(tmpBuffer, NULL, 16);
	}
}

int main(int argc, char *argv[])
{

	//////////////////////////////////////////////////////////////////////////////////

	pid_t pid;
	off_t MemAddress;
	unsigned long PathSize;

	int fd;
	char mFileName[50];
	size_t nByte;
	
	char* strBuffer = (char*) malloc(STR_BUFFER_SIZE);
	char tmpBuffer[50];

	memset(strBuffer, 0, STR_BUFFER_SIZE);

	unsigned char OpcodeBuffer[OPCODE_BUFFER_SIZE];
	unsigned char OpcodePatch[OPCODE_BUFFER_SIZE];

	if (argc != 5)
	{
		printf("[*] Help\n");
		printf("[*] application [PID] [Address] [Path Size] [Path Data]\n");
		exit(0);
	}

	pid 			= (unsigned long) atoi(argv[1]);
	MemAddress 		= strtoul(argv[2], NULL, 16);
	PathSize 		= (unsigned long) atoi(argv[3]);

	PathDataParser(argv[4], PathSize, OpcodePatch);

	strcpy(strBuffer, "==============================================================\n");

	//////////////////////////////////////////////////////////////////////////////////

	sprintf(mFileName, "/proc/%d/mem", pid);
	if ((fd = open(mFileName, O_RDWR | O_LARGEFILE)) <= 0)
	{
		printf("Failed Open Mem\n");
	}

	if (ptrace(PTRACE_ATTACH, pid, 0, 0) < 0)
	{
		printf("Ptrace Attach Failed\n");

		free(strBuffer);
		return 0;
	}

	waitpid(pid, NULL, WUNTRACED);
	
	//////////////////////////////////////////////////////////////////////////////////

	sprintf(tmpBuffer, "Before: 0x%08lX\n\t", MemAddress);
	strcat(strBuffer, tmpBuffer);

	lseek(fd, MemAddress, SEEK_SET);
	if ((nByte = read(fd, OpcodeBuffer, PathSize)) <= 0)
	{
		printf("Failed Read\n");
	}

	for (int i=0; i<PathSize + 4; i++)
	{
		sprintf(tmpBuffer, "%02X ", OpcodeBuffer[i]);
		strcat(strBuffer, tmpBuffer);
	}
	strcat(strBuffer, "\n\n");

	//////////////////////////////////////////////////////////////////////////////////

	lseek(fd, MemAddress, SEEK_SET);
	if ((nByte = write(fd, OpcodePatch, PathSize)) <= 0)
	{
		printf("Failed Write\n");
	}

	strcat(strBuffer, "Patch:\t");
	for (int i=0; i<PathSize; i++)
	{
		sprintf(tmpBuffer, "%02X ", OpcodePatch[i]);
		strcat(strBuffer, tmpBuffer);
	}
	strcat(strBuffer, "\n\n");

	//////////////////////////////////////////////////////////////////////////////////

	sprintf(tmpBuffer, "After: 0x%08lX\n\t", MemAddress);
	strcat(strBuffer, tmpBuffer);

	lseek(fd, MemAddress, SEEK_SET);
	if ((nByte = read(fd, OpcodeBuffer, PathSize)) < 0)
	{
		printf("Failed Read\n");
	}

	for (int i=0; i<PathSize + 4; i++)
	{
		sprintf(tmpBuffer, "%02X ", OpcodeBuffer[i]);
		strcat(strBuffer, tmpBuffer);
	}
	
	//////////////////////////////////////////////////////////////////////////////////

	printf("%s\n", strBuffer);

	ptrace(PTRACE_DETACH, pid, 0, 0);

	close(fd);
	free(strBuffer);

	return 0;

	//////////////////////////////////////////////////////////////////////////////////
}