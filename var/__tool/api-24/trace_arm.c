#define _GNU_SOURCE

//////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>
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
	
	struct pt_regs regs;

	int w;
	int status;


	if (argc != 4)
	{
		printf("[*] Help\n");
		printf("[*] application [PID] [StartAddress] [Size]\n");
		exit(0);
	}

	pid 				= (unsigned long) atoi(argv[1]);
	MemAddress 			= strtoul(argv[2], NULL, 16);
	ReadBufferSize 		= (unsigned long) atoi(argv[3]);

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
						"[ORIG_R0]: 0x%08X\t[R0]: 0x%08X\t[R1]: 0x%08X\t[R2]: 0x%08X\t[R3]: 0x%08X\t[R4]: 0x%08X\n"
						"[R5]: 0x%08X\t[R6]: 0x%08X\t[R7]: 0x%08X\t[R8]: 0x%08X\t[R9]: 0x%08X\t[R10]: 0x%08X\n"
						"[SP]: 0x%08X\t[FP]: 0x%08X\t[IP]: 0x%08X\t[LR]: 0x%08X\t[PC]: 0x%08X\t[CPSR]: 0x%08X\n"
						"====================================================================================================================\n",
				regs.ARM_ORIG_r0, regs.ARM_r0, regs.ARM_r1, regs.ARM_r2, regs.ARM_r3, regs.ARM_r4,
				regs.ARM_r5,regs.ARM_r6, regs.ARM_r7, regs.ARM_r8, regs.ARM_r9, regs.ARM_r10,
				regs.ARM_sp, regs.ARM_fp, regs.ARM_ip, regs.ARM_lr, regs.ARM_pc, regs.ARM_cpsr);
		

		lseek(fd, MemAddress, SEEK_SET);
		if ((nByte = write(fd, orgOpcode, ReadBufferSize)) == -1 )
		{
			printf("[%d] Failed register Write\n", errno);
			exit(0);
		}

		regs.ARM_pc = MemAddress;
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
