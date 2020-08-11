#define PY_SSIZE_T_CLEAN

#include "elfformat.h"

#define ELFMAGIC_SIZE 					sizeof(ElfMagic)-1
#define HEADER_SIZE						500
#define PROGRAM_SIZE					3000
#define SECTION_SIZE					3000

#define STRING_SIZE						20


PyObject* ElfFormatException = NULL;


char* GetSetionName(unsigned char*		pchBuffer,
				  struct Elf32_Ehdr*	e32_ehdr,
				  Elf32_Word  			SectionHeaderName)
{
	Elf32_Off TableOffset = e32_ehdr->e_shoff + (e32_ehdr->e_shentsize * e32_ehdr->e_shstrndx);

	struct Elf32_Shdr e32_shdr;
	//int l = 0;

	memset(&e32_shdr, 0, sizeof(struct Elf32_Shdr));
	memcpy(&e32_shdr,
			pchBuffer + TableOffset,
			sizeof(struct Elf32_Shdr));

	TableOffset = e32_shdr.sh_offset + SectionHeaderName;

	//l = strlen((char*)(pchBuffer + TableOffset));
	char* pchStrBuffer = (char*) malloc(sizeof(char) * STRING_SIZE);
	strcpy(pchStrBuffer, (char*)(pchBuffer + TableOffset));

	return pchStrBuffer;
}


int ShrParser(unsigned char* 		pchBuffer,
			  struct Elf32_Ehdr* 	e32_ehdr,
			  char* 				pchShrBuffer)
{
	Elf32_Off StartSetionHeaderTable 	= e32_ehdr->e_shoff;
	Elf32_Half SetionHeaderTableSize 	= e32_ehdr->e_shentsize;
	Elf32_Half SetionHeaderTableNumber 	= e32_ehdr->e_shnum;


	Elf32_Off TableOffset = 0;

	struct Elf32_Shdr e32_shdr;


	char* 	tmpStrBuffer;
	char*  	pchShrTmpBuffer = (char*) malloc(sizeof(char) * 150);
	//memset(pchShrTmpBuffer, 0, sizeof(char) * 150);


	strcpy(pchShrBuffer,
			"Section Headers:\n"
			"[Nr] Name                   Type            Addr     Off    Size   Al\n");


	for(int i=0; i<SetionHeaderTableNumber; i++)
	{
		TableOffset = StartSetionHeaderTable + (i*SetionHeaderTableSize);

		//memset(&e32_shdr, 0, sizeof(struct Elf32_Shdr));
		memcpy(&e32_shdr,
				pchBuffer + TableOffset,
				sizeof(struct Elf32_Shdr));

		tmpStrBuffer = GetSetionName(pchBuffer, e32_ehdr, e32_shdr.sh_name);

		sprintf(pchShrTmpBuffer,
			"[%2d] %-22s %-15s %08x %06x %06x %2d\n",

			i,
			tmpStrBuffer,
			SECTION_TYPE[e32_shdr.sh_type].c_str(),
			e32_shdr.sh_addr,
			e32_shdr.sh_offset,
			e32_shdr.sh_size,
			e32_shdr.sh_addralign
		);

		strcat(pchShrBuffer, pchShrTmpBuffer);
		free(tmpStrBuffer);
	}


	free(pchShrTmpBuffer);

	return 0;
}


int PhrParser(unsigned char* 		pchBuffer,
			  struct Elf32_Ehdr* 	e32_ehdr,
			  char* 				pchPhrBuffer)
{
	Elf32_Off StartProcessHeaderTable 	= e32_ehdr->e_phoff;
	Elf32_Half ProcessHeaderTableSize 	= e32_ehdr->e_phentsize;
	Elf32_Half ProcessHeaderTableNumber = e32_ehdr->e_phnum;

	Elf32_Off TableOffset = 0;

	struct Elf32_Phdr e32_phdr;

	char*  pchPhrTmpBuffer = (char*) malloc(sizeof(char) * 150);
	//memset(pchPhrTmpBuffer, 0, sizeof(char) * 150);

	strcpy(pchPhrBuffer,
			"Program Headers:\n"
			"Type\t\tOffset   VirtAddr   PhysAddr   FileSiz MemSiz  Flg Align\n");


	for(int i=0; i<ProcessHeaderTableNumber; i++)
	{
		TableOffset = StartProcessHeaderTable + (i*ProcessHeaderTableSize);

		//memset(&e32_phdr, 0, sizeof(struct Elf32_Phdr));
		memcpy(&e32_phdr,
				pchBuffer + TableOffset,
				sizeof(struct Elf32_Phdr));

		sprintf(pchPhrTmpBuffer,
				"%-8s\t0x%06x 0x%08x 0x%08x 0x%05x 0x%05x %-3s 0x%x\n",

				PROGRAM_TYPE[e32_phdr.p_type].c_str(),
				e32_phdr.p_offset,
				e32_phdr.p_vaddr,
				e32_phdr.p_paddr,
				e32_phdr.p_filesz,
				e32_phdr.p_memsz,
				PROGRAM_FLAG[e32_phdr.p_flags].c_str(),
				e32_phdr.p_align
		);

		strcat(pchPhrBuffer, pchPhrTmpBuffer);
	}


	free(pchPhrTmpBuffer);

	return 0;
}


int EhrParser(unsigned char* 		pchBuffer,
			  struct Elf32_Ehdr* 	e32_ehdr,
			  char* 				pchEhrBuffer)
{
	//memset(e32_ehdr, 0, 		sizeof(struct Elf32_Ehdr));
	memcpy(e32_ehdr, pchBuffer, sizeof(struct Elf32_Ehdr));

	sprintf(pchEhrBuffer, "Elf Header:\n"
						"  Magic:\t\t\t\t%02x %02x %02x %02x\n"
						"  Class:\t\t\t\t%s\n"
						"  OS/ABI:\t\t\t\t%s\n"
						"  Machine:\t\t\t\t%s\n"
						"  Type:\t\t\t\t\t%s\n"
						"  Entry point address:\t\t\t0x%02x\n"
						"  Start of program headers:\t\t%d (bytes into file)\n"
						"  Start of section headers:\t\t%d (bytes into file)\n"
						"  Size of this header:\t\t\t%d (bytes)\n"
						"  Size of program headers:\t\t%d (bytes)\n"
						"  Number of program headers:\t\t%d\n"
						"  Size of section headers:\t\t%d (bytes)\n"
						"  Number of section headers:\t\t%d\n"
						"  Section header string table index:\t%d\n",
		
			e32_ehdr->e_ident[EI_MAG0],
			e32_ehdr->e_ident[EI_MAG1],
			e32_ehdr->e_ident[EI_MAG2],
			e32_ehdr->e_ident[EI_MAG3],

			OBJECT_FILE_CLASS[e32_ehdr->e_ident[EI_CLASS]].c_str(),
			OS_ABI[e32_ehdr->e_ident[EI_OSABI]].c_str(),
			MACHINE_ARCHITECTURES[e32_ehdr->e_machine].c_str(),
			FILE_TYPE[e32_ehdr->e_type].c_str(),

			e32_ehdr->e_entry,
			e32_ehdr->e_phoff,
			e32_ehdr->e_shoff,
			e32_ehdr->e_ehsize,
			e32_ehdr->e_phentsize,
			e32_ehdr->e_phnum,
			e32_ehdr->e_shentsize,
			e32_ehdr->e_shnum,
			e32_ehdr->e_shstrndx
	);


	return 0;
}


static PyObject *
parser(PyObject* self, PyObject* a_args)
{
	FILE* 			pstRStream 	= NULL;
	unsigned char* 	pchBuffer	= NULL;

	const char* args;
	Py_ssize_t args_size;


	if(!PyArg_ParseTuple(a_args, "s#", &args, &args_size))
	{
		ELFFORMAT_EXCEPTION(-1, "ARGS PASS FAILED!!!\n");
		return NULL;
	}
	else
	{
		pstRStream 	= fopen(args, "rb");
	}


	if(pstRStream != NULL)
	{
		fseek(pstRStream, 0, SEEK_END);
		long nBytes = ftell(pstRStream);

		pchBuffer 	= (unsigned char*) malloc(sizeof(unsigned char) * nBytes);

		fseek(pstRStream, 0, SEEK_SET);
		fread(pchBuffer, sizeof(unsigned char), nBytes, pstRStream);

		fclose(pstRStream);
	}
	else
	{
		ELFFORMAT_EXCEPTION(-1, "FILE OPEN FAILED!!!\n");

		return 0;
	}


	struct 			Elf32_Ehdr e32_ehdr;
	char*			pchEhrBuffer = (char*) malloc(sizeof(char) * HEADER_SIZE);
	char*			pchPhrBuffer = (char*) malloc(sizeof(char) * PROGRAM_SIZE);
	char*			pchShrBuffer = (char*) malloc(sizeof(char) * SECTION_SIZE);


	memset(pchEhrBuffer, 0, sizeof(char) * HEADER_SIZE);
	memset(pchPhrBuffer, 0, sizeof(char) * PROGRAM_SIZE);
	memset(pchShrBuffer, 0, sizeof(char) * SECTION_SIZE);


	EhrParser(pchBuffer, &e32_ehdr, pchEhrBuffer);
	PhrParser(pchBuffer, &e32_ehdr, pchPhrBuffer);
	ShrParser(pchBuffer, &e32_ehdr, pchShrBuffer);

	//printf("%s\n", pchEhrBuffer);
	//printf("%s\n", pchPhrBuffer);
	//printf("%s\n", pchShrBuffer);

	//free(pchEhrBuffer);
	//free(pchPhrBuffer);
	//free(pchShrBuffer);

	free(pchBuffer);

	return Py_BuildValue("sss", pchEhrBuffer, pchPhrBuffer, pchShrBuffer);
}


static PyMethodDef ElfFormatMethods[] = {
	{"parser", parser, METH_VARARGS, "ELF Parser"},
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef elfformatmodule = {
	PyModuleDef_HEAD_INIT,
	"elfformat",
	NULL,
	-1,
	ElfFormatMethods
};


PyMODINIT_FUNC
PyInit_elfformat(void)
{
	PyObject* m = NULL;


	if(NULL == (m = PyModule_Create(&elfformatmodule)))
	{
		DEPRINT("ElfFormatException Module Exception");
		return NULL;
	}

	if (NULL == (ElfFormatException = PyErr_NewException("ElfFormatException.Exception",
													PyExc_Exception,
													NULL)))
	{
		DEPRINT("NewException");
		return NULL;
	}

	Py_INCREF(ElfFormatException);

	if (PyModule_AddObject(m, "ElfFormatException", ElfFormatException) < 0)
	{
		Py_DECREF(ElfFormatException);
		Py_CLEAR(ElfFormatException);
		Py_DECREF(m);

		return NULL;
	}

	return m;
}
