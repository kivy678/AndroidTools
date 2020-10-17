#define PY_SSIZE_T_CLEAN

//////////////////////////////////////////////////////////////////////////////////

#include "elfformat.h"
#include "parser.h"

#define ELFMAGIC_SIZE 					sizeof(ElfMagic)-1
#define HEADER_SIZE						500
#define PROGRAM_SIZE					3000
#define SECTION_SIZE					3000
#define DYNAMIC_SIZE					3000
#define SYMTAB_SIZE						500000
#define REL_SIZE						500000

//////////////////////////////////////////////////////////////////////////////////

PyObject* ElfFormatException = NULL;

//////////////////////////////////////////////////////////////////////////////////


int HeapFree(unsigned char* pchBuffer,
			 char* pchEhrBuffer,
			 char* pchPhrBuffer,
			 char* pchShrBuffer,
			 char* pchDynBuffer,
			 char* pchSymBuffer,
			 char* pchDsymBuffer,
			 char* pchRelBuffer,
			 char* pchRelpBuffer,
			 struct Elf32_Section_Linker* 	e32_section_linker,
			 struct Elf32_Dyn_Linker* 		e32_dyn_linker,
			 struct Elf32_Sym_Linker* 		e32_sym_linker,
			 struct Elf32_Sym_Linker* 		e32_dsym_linker,
			 struct Elf32_Rel_Linker* 		e32_rel_linker,
			 struct Elf32_Rel_Linker* 		e32_relp_linker)
{

	struct Elf32_Section_Linker* 	NextNode1 = NULL;
	struct Elf32_Dyn_Linker* 		NextNode2 = NULL;
	struct Elf32_Sym_Linker* 		NextNode3 = NULL;
	struct Elf32_Rel_Linker* 		NextNode4 = NULL;

	free(pchBuffer);

	free(pchEhrBuffer);
	free(pchPhrBuffer);
	free(pchShrBuffer);
	free(pchDynBuffer);
	free(pchSymBuffer);
	free(pchDsymBuffer);
	free(pchRelBuffer);
	free(pchRelpBuffer);

		
	while(e32_section_linker->nextPoint != NULL)
	{
		NextNode1 = e32_section_linker->nextPoint;
		free(e32_section_linker);

		e32_section_linker = NextNode1;
	}
	free(e32_section_linker);


	while(e32_dyn_linker->nextPoint != NULL)
	{
		NextNode2 = e32_dyn_linker->nextPoint;
		free(e32_dyn_linker);

		e32_dyn_linker = NextNode2;
	}
	free(e32_dyn_linker);


	while(e32_sym_linker->nextPoint != NULL)
	{
		NextNode3 = e32_sym_linker->nextPoint;
		free(e32_sym_linker);

		e32_sym_linker = NextNode3;
	}
	free(e32_sym_linker);


	while(e32_dsym_linker->nextPoint != NULL)
	{
		NextNode3 = e32_dsym_linker->nextPoint;
		free(e32_dsym_linker);

		e32_dsym_linker = NextNode3;
	}
	free(e32_dsym_linker);


	while(e32_rel_linker->nextPoint != NULL)
	{
		NextNode4 = e32_rel_linker->nextPoint;
		free(e32_rel_linker);

		e32_rel_linker = NextNode4;
	}
	free(e32_rel_linker);


	while(e32_relp_linker->nextPoint != NULL)
	{
		NextNode4 = e32_relp_linker->nextPoint;
		free(e32_relp_linker);

		e32_relp_linker = NextNode4;
	}
	free(e32_relp_linker);


	return 0;
}


static PyObject *
parser(PyObject* self, PyObject* a_args)
{

	//////////////////////////////////////////////////////////////////////////////////

	PyObject* 		returnString = NULL;
	FILE* 			pstRStream 	= NULL;
	unsigned char* 	pchBuffer	= NULL;

	const char* 	args		= NULL;
	const char*		option		= NULL;

	struct Elf32_Ehdr 				e32_ehdr 			= {0};
	struct Elf32_Phdr 				e32_phdr 			= {0};
	struct Elf32_Section_Linker* 	e32_section_linker 	= NULL;
	struct Elf32_Dyn_Linker* 		e32_dyn_linker 		= NULL;
	struct Elf32_Sym_Linker* 		e32_sym_linker 		= NULL;
	struct Elf32_Sym_Linker* 		e32_dsym_linker 	= NULL;
	struct Elf32_Rel_Linker* 		e32_rel_linker 		= NULL;
	struct Elf32_Rel_Linker* 		e32_relp_linker 	= NULL;


	char*	pchEhrBuffer 	= (char*) malloc(sizeof(char) * HEADER_SIZE);
	char*	pchPhrBuffer 	= (char*) malloc(sizeof(char) * PROGRAM_SIZE);
	char*	pchShrBuffer 	= (char*) malloc(sizeof(char) * SECTION_SIZE);
	char*	pchDynBuffer 	= (char*) malloc(sizeof(char) * DYNAMIC_SIZE);
	char*	pchSymBuffer 	= (char*) malloc(sizeof(char) * SYMTAB_SIZE);
	char*	pchDsymBuffer 	= (char*) malloc(sizeof(char) * SYMTAB_SIZE);
	char*	pchRelBuffer 	= (char*) malloc(sizeof(char) * REL_SIZE);
	char*	pchRelpBuffer 	= (char*) malloc(sizeof(char) * REL_SIZE);


	memset(pchEhrBuffer, 0, sizeof(char) * HEADER_SIZE);
	memset(pchPhrBuffer, 0, sizeof(char) * PROGRAM_SIZE);
	memset(pchShrBuffer, 0, sizeof(char) * SECTION_SIZE);
	memset(pchDynBuffer, 0, sizeof(char) * DYNAMIC_SIZE);
	memset(pchSymBuffer, 0, sizeof(char) * SYMTAB_SIZE);
	memset(pchDsymBuffer, 0, sizeof(char) * SYMTAB_SIZE);
	memset(pchRelBuffer, 0, sizeof(char) * REL_SIZE);
	memset(pchRelpBuffer, 0, sizeof(char) * REL_SIZE);


	e32_section_linker = (struct Elf32_Section_Linker*) malloc(sizeof(struct Elf32_Section_Linker));
	memset(e32_section_linker, 0, sizeof(struct Elf32_Section_Linker));

	e32_dyn_linker = (struct Elf32_Dyn_Linker*) malloc(sizeof(struct Elf32_Dyn_Linker));
	memset(e32_dyn_linker, 0, sizeof(struct Elf32_Dyn_Linker));

	e32_sym_linker = (struct Elf32_Sym_Linker*) malloc(sizeof(struct Elf32_Sym_Linker));
	memset(e32_sym_linker, 0, sizeof(struct Elf32_Sym_Linker));

	e32_dsym_linker = (struct Elf32_Sym_Linker*) malloc(sizeof(struct Elf32_Sym_Linker));
	memset(e32_dsym_linker, 0, sizeof(struct Elf32_Sym_Linker));

	e32_rel_linker = (struct Elf32_Rel_Linker*) malloc(sizeof(struct Elf32_Rel_Linker));
	memset(e32_rel_linker, 0, sizeof(struct Elf32_Rel_Linker));

	e32_relp_linker = (struct Elf32_Rel_Linker*) malloc(sizeof(struct Elf32_Rel_Linker));
	memset(e32_relp_linker, 0, sizeof(struct Elf32_Rel_Linker));


	//////////////////////////////////////////////////////////////////////////////////

	if(!PyArg_ParseTuple(a_args, "ss", &args, &option))
	{
		ELFFORMAT_EXCEPTION(-1, "ARGS PASS FAILED!!!\n");
		return NULL;
	}
	else
	{
		pstRStream 	= fopen(args, "rb");
	}

	//////////////////////////////////////////////////////////////////////////////////

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

		free(pchBuffer);

		return 0;
	}

	//////////////////////////////////////////////////////////////////////////////////

	EhrParser(pchBuffer, &e32_ehdr, pchEhrBuffer);

	if (strcmp(OBJECT_FILE_CLASS[e32_ehdr.getFileClass()].c_str(), "ELF32") == 0)
	{
		PhrParser(pchBuffer, &e32_ehdr, &e32_phdr, pchPhrBuffer);
		ShrParser(pchBuffer, &e32_ehdr, e32_section_linker, pchShrBuffer);
		DynParser(pchBuffer, &e32_ehdr, e32_dyn_linker, pchDynBuffer);
		SymParser(pchBuffer, &e32_ehdr, e32_section_linker, e32_sym_linker, pchSymBuffer, ".symtab");
		SymParser(pchBuffer, &e32_ehdr, e32_section_linker, e32_dsym_linker, pchDsymBuffer, ".dynsym");
		RelParser(pchBuffer, &e32_ehdr, e32_section_linker, e32_dsym_linker, e32_rel_linker, pchRelBuffer, ".rel.dyn");
		RelParser(pchBuffer, &e32_ehdr, e32_section_linker, e32_dsym_linker, e32_relp_linker, pchRelpBuffer, ".rel.plt");
	}


	//////////////////////////////////////////////////////////////////////////////////

	if (strcmp(option, "h") == 0)
		returnString = Py_BuildValue("s", pchEhrBuffer);

	else if (strcmp(OBJECT_FILE_CLASS[e32_ehdr.getFileClass()].c_str(), "ELF64") == 0)
		returnString = Py_BuildValue("s", pchEhrBuffer);

	else if (strcmp(option, "p") == 0)
		returnString = Py_BuildValue("s", pchPhrBuffer);

	else if (strcmp(option, "s") == 0)
		returnString = Py_BuildValue("s", pchShrBuffer);

	else if (strcmp(option, "d") == 0)
		returnString = Py_BuildValue("s", pchDynBuffer);

	else if (strcmp(option, "S") == 0)
		returnString = Py_BuildValue("s", pchSymBuffer);

	else if (strcmp(option, "dS") == 0)
		returnString = Py_BuildValue("s", pchDsymBuffer);

	else if (strcmp(option, "r") == 0)
		returnString = Py_BuildValue("s", pchRelBuffer);

	else if (strcmp(option, "rp") == 0)
		returnString = Py_BuildValue("s", pchRelpBuffer);

	else
		returnString = Py_BuildValue("sss", pchEhrBuffer, pchPhrBuffer, pchShrBuffer);


	HeapFree(pchBuffer,
			 pchEhrBuffer,
			 pchPhrBuffer,
			 pchShrBuffer,
			 pchDynBuffer,
			 pchSymBuffer,
			 pchDsymBuffer,
			 pchRelBuffer,
			 pchRelpBuffer,
			 e32_section_linker,
			 e32_dyn_linker,
			 e32_sym_linker,
			 e32_dsym_linker,
			 e32_rel_linker,
			 e32_relp_linker);


	return returnString;

}


//////////////////////////////////////////////////////////////////////////////////

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

//////////////////////////////////////////////////////////////////////////////////
