#define _GNU_SOURCE

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

#include <errno.h>
#include <sys/user.h>

/////////////////////////////////////////////////////////////////////////////

int ProcessAttch(pid_t);
int ProcessDetach(pid_t);
int ProcessRun(pid_t);
unsigned char* setBreakPoint(int, off_t, unsigned long);

/////////////////////////////////////////////////////////////////////////////

int main(int argc, char *argv[])
{

	/////////////////////////////////////////////////////////////////////////////

	pid_t pid;
	off_t MemAddress;
	unsigned long ReadBufferSize;

	int fd;
	char mFileName[50] = {0};
	size_t nByte;
	
	struct user_regs_struct regs;

	int w;
	int status;
	

	if (argc != 4)
	{
		printf("[*] Help\n");
		printf("[*] application [PID] [StartAddress] [Size]\n");
		exit(0);
	}

	pid 			= (unsigned long) atoi(argv[1]);
	MemAddress 		= strtoul(argv[2], NULL, 16);
	ReadBufferSize 	= (unsigned long) atoi(argv[3]);

	if (ProcessAttch(pid) < 0)
	{
		exit(0); 
	}

	/////////////////////////////////////////////////////////////////////////////

	sprintf(mFileName, "/proc/%d/mem", pid);

	if ((fd = open(mFileName, O_RDWR | O_LARGEFILE)) == -1 )
	{
		printf("[%d] Failed Open Mem\n", errno);
		exit(0);
	}

	/////////////////////////////////////////////////////////////////////////////

	unsigned char* orgOpcode = setBreakPoint(fd, MemAddress, ReadBufferSize);

	/////////////////////////////////////////////////////////////////////////////

	if (ProcessRun(pid) == SIGTRAP)
	{

		ptrace(PTRACE_GETREGS, pid, 0, &regs);
		fprintf(stderr, "====================================================================================================================\n"
						"[ORIG_EAX]: 0x%08X\t[EAX]: 0x%08X\t[EBX]: 0x%08X\t[ECX]: 0x%08X\t[EDX]: 0x%08X\n"
						"[ESI]: 0x%08X\t[EDI]: 0x%08X\t[EIP]: 0x%08X\t[ESP]: 0x%08X\t[XDS]: 0x%08X\n"
						"[XES]: 0x%08X\t[XGS]: 0x%08X\t[XCS]: 0x%08X\t[XSS]: 0x%08X\t[ELFAGS]: 0x%08X\n"
						"====================================================================================================================\n",
				regs.orig_eax, regs.eax, regs.ebx, regs.ecx, regs.edx, regs.esi, regs.edi, regs.eip, regs.esp,
				regs.xds, regs.xes, regs.xgs, regs.xcs, regs.xss, regs.eflags);
		

		lseek(fd, MemAddress, SEEK_SET);
		if ((nByte = write(fd, orgOpcode, ReadBufferSize)) == -1 )
		{
			printf("[%d] Failed register Write\n", errno);
			exit(0);
		}

		regs.eip = MemAddress;
		ptrace(PTRACE_SETREGS, pid, 0, &regs);

		free(orgOpcode);	
	}

	/////////////////////////////////////////////////////////////////////////////

	close(fd);

	ProcessDetach(pid);
	printf("Main End\n");

	return 0;
}

/////////////////////////////////////////////////////////////////////////////

unsigned char* setBreakPoint(int fd, off_t MemAddress, unsigned long ReadBufferSize)
{
	size_t nByte;
	unsigned char* orgOpcode = (unsigned char*) malloc(ReadBufferSize+1);
	memset(orgOpcode, 0, ReadBufferSize+1);
	
	lseek(fd, MemAddress, SEEK_SET);

	if ((nByte = read(fd, orgOpcode, ReadBufferSize)) == -1 )
	{
		printf("[%d] Failed Read\n", errno);
		exit(0);
	}

	for (int i=0; i<nByte; i++)
	{
		fprintf(stderr, "%02X ", orgOpcode[i]);
	}

	lseek(fd, MemAddress, SEEK_SET);
	if ((nByte = write(fd, "\xCC", ReadBufferSize)) == -1 )
	{
		printf("[%d] Failed Write\n", errno);
		exit(0);
	}

	return orgOpcode;
}


int ProcessAttch(pid_t pid)
{
	int w;
	int status;

	if (ptrace(PTRACE_ATTACH, pid, 0, 0) < 0)
	{
		printf("[%d] Ptrace Attach Failed\n", errno);
		return -1;
	}

	w = waitpid(pid, &status, WUNTRACED);	
	//printf("[%d] [%d] AttachWait\n", w, WIFSTOPPED(status));

	return 0;
}


int ProcessDetach(pid_t pid)
{
	ptrace(PTRACE_DETACH, pid, 0, 0);

	return 0;
}


int ProcessRun(pid_t pid)
{
	int w;
	int status;

	ptrace(PTRACE_CONT, pid, 0, 0);
	printf("Running Process\n");

	w = waitpid(pid, &status, WUNTRACED);
	printf("[%d] [%d] RunWait\n", w, WSTOPSIG(status));

	return WSTOPSIG(status);
}
