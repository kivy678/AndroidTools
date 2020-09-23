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

#define STR_ReadBuffer 	sizeof(char) * 200

//////////////////////////////////////////////////////////////////////////////////


int GetBinary(pid_t pid, struct iovec* local, struct iovec* remote)
{
	ssize_t nread;

	if ((nread = process_vm_readv(pid, local, 1, remote, 1, 0)) <= 0)
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
	off_t MemAddress;
	unsigned long ReadBuffer;
	
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

	struct iovec local[1];
	struct iovec remote[1];
	unsigned char buffer[ReadBuffer];
	
	local[0].iov_base	= buffer;
	local[0].iov_len 	= ReadBuffer;
	
	remote[0].iov_base 	= (void*) MemAddress;
	remote[0].iov_len 	= ReadBuffer;

	if (GetBinary(pid, local, remote) <= 0)
	{
		return -1;
	}

	//////////////////////////////////////////////////////////////////////////////////

	strcat(strBuffer, tmpBuffer);

	for (int i=0; i<ReadBuffer; i++)
	{
		sprintf(tmpBuffer, "%02X ", buffer[i]);
		strcat(strBuffer, tmpBuffer);
	}

	//////////////////////////////////////////////////////////////////////////////////

	printf("%s\n", strBuffer);

//	ptrace(PTRACE_DETACH, pid, 0, 0);

	free(strBuffer);

	return 0;

	//////////////////////////////////////////////////////////////////////////////////

}