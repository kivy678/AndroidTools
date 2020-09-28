#define _GNU_SOURCE

//////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/uio.h>

#include <sys/ptrace.h>
#include <sys/wait.h>

#include <errno.h>

//////////////////////////////////////////////////////////////////////////////////

#define BUFFER_SIZE 		16
#define STR_BUFFER_SIZE 	sizeof(char) * 5000

//////////////////////////////////////////////////////////////////////////////////


int GetBinary(pid_t pid, struct iovec* local, struct iovec* remote)
{
	ssize_t nread;

	if ((nread = process_vm_readv(pid, local, 1, remote, 1, 0)) == -1)
	{
		printf("[%d] Failed Read\n", errno);

		return -1;
	}
	else
	{
		//printf("[DBG] nread: %d\n", nread);
	}

	return nread;
}


int main(int argc, char *argv[])
{

	//////////////////////////////////////////////////////////////////////////////////

	pid_t pid;
	off_t MemStartAddr;
	unsigned long PrintRow;
	off_t MemAddress;
	
	char* strBuffer = (char*) malloc(STR_BUFFER_SIZE);
	char tmpBuffer[50] = {0};

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
	struct iovec local[1] = {0};
	struct iovec remote[1] = {0};
	unsigned char buffer[BUFFER_SIZE+1] = {0};
	
	local[0].iov_base	= buffer;
	local[0].iov_len 	= BUFFER_SIZE;
	
GET_BIN:
	remote[0].iov_base 	= (void*) MemAddress;
	remote[0].iov_len 	= BUFFER_SIZE;

	if (GetBinary(pid, local, remote) < 0)
	{
		return -1;
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

	free(strBuffer);

	return 0;

	//////////////////////////////////////////////////////////////////////////////////

}