#define _GNU_SOURCE
#define _LARGEFILE64_SOURCE

//////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <fcntl.h>
#include <unistd.h>

#include <sys/ptrace.h>
#include <sys/wait.h>

//////////////////////////////////////////////////////////////////////////////////

#define READ_SIZE 	4096
#define SAVE_PATH	"/data/local/tmp/dump.bin"

//////////////////////////////////////////////////////////////////////////////////

int main(int argc, char *argv[])
{

	//////////////////////////////////////////////////////////////////////////////////

	pid_t pid;
	off_t StartAddress;
	off_t EndAddress;

	int fd;
	char mFileName[50] = {0};
	int fw;

	ssize_t nBytes = 0;

	unsigned char* strBuffer = (unsigned char*) malloc(READ_SIZE);
	memset(strBuffer, 0, READ_SIZE);


	if (argc != 4)
	{
		printf("[*] Help\n");
		printf("[*] application [PID] [Start Address] [End Address]\n");
		exit(0);
	}

	pid 			= (unsigned long) atoi(argv[1]);
	StartAddress 	= strtoul(argv[2], NULL, 16);
	EndAddress 		= strtoul(argv[3], NULL, 16);

	//////////////////////////////////////////////////////////////////////////////////

	sprintf(mFileName, "/proc/%d/mem", pid);

	if ((fd = open(mFileName, O_RDONLY|O_LARGEFILE)) == -1 ||
		(fw = open(SAVE_PATH, O_RDWR|O_CREAT|O_TRUNC|O_LARGEFILE)) == -1)
	{
		printf("Failed Open Mem\n");

		free(strBuffer);
		return -1;
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

	lseek(fd, StartAddress, SEEK_SET);

	while (StartAddress < EndAddress)
	{
		if ((nBytes = read(fd, strBuffer, READ_SIZE)) > 0 )
		{
			write(fw, strBuffer, nBytes);
		}
		else
		{	
			break;
		}

		StartAddress += READ_SIZE;
	}

	//////////////////////////////////////////////////////////////////////////////////

	close(fd);
	close(fw);

	free(strBuffer);

	printf("Main done\n");

	return 0;
}
